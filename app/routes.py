from flask import abort
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app import create_app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Image, Tag
from flask import Blueprint
from flask import current_app
from werkzeug.utils import secure_filename
import os
import uuid
from PIL import Image as PILImage
from PIL import ExifTags
from datetime import datetime
from sqlalchemy import or_
from PIL import ImageEnhance
import os
from transformers import pipeline
os.environ["TRANSFORMERS_OFFLINE"] = "1" # 关闭联网尝试
os.environ["HF_DATASETS_OFFLINE"] = "1"

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) # 指定本地模型路径
MODEL_PATH = os.path.join(os.path.dirname(BASE_DIR), "vit-model")
try:
    print(f"正在从本地加载 AI 模型: {MODEL_PATH}")
    classifier = pipeline( # 将本地路径传给 model 参数
        "image-classification", 
        model=MODEL_PATH
    )
    print("AI 模型本地加载成功！")
except Exception as e:
    print(f"AI 模型本地加载失败，请确认文件路径正确: {e}")
    classifier = None

def get_ai_tags(image_path): # AI 识别
    if not classifier:
        return []
    try:
        results = classifier(image_path)
        tags = [res['label'].split(',')[0] for res in results if res['score'] > 0.15] # 筛选得分超过 0.15 的标签
        return tags[:3]
    except Exception as e:
        print(f"识别图片时出错: {e}")
        return []

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_or_create_tag(name):
    """如果标签存在就获取，不存在就创建"""
    name = name.strip() # 移除首尾空格并确保不为空
    if not name:
        return None
    tag = Tag.query.filter_by(name=name).first() # 查找现有标签
    if not tag:
        tag = Tag(name=name) # 如果没有，创建一个新的
        db.session.add(tag)
    return tag

def process_and_save_image(file_storage, user_id):
    try:
        # 保存原图
        ext = file_storage.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{ext}"
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file_storage.save(save_path)

        # 提取 EXIF
        img = PILImage.open(save_path)
        resolution = f"{img.width}x{img.height}"
        exif_datetime = None
        try:
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = ExifTags.TAGS.get(tag_id, tag_id)
                    if tag == 'DateTimeOriginal':
                        exif_datetime = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                        break
        except Exception as e:
            print(f"EXIF提取失败: {e}")

        # 生成缩略图
        thumb_filename = f"thumb_{unique_filename}"
        thumb_path = os.path.join(current_app.config['THUMBNAIL_FOLDER'], thumb_filename)
        img.thumbnail((300, 300))
        img.save(thumb_path)

        # 创建图片对象
        original_name = file_storage.filename.rsplit('.', 1)[0]
        new_image = Image(
            filename=unique_filename,
            thumbnail=thumb_filename,
            user_id=user_id,
            resolution=resolution,
            exif_datetime=exif_datetime,
            name=original_name
        )
        db.session.add(new_image)

        # 自动打标逻辑
        if exif_datetime:
            year_str = str(exif_datetime.year)
        else:
            year_str = str(datetime.now().year)
        tag = get_or_create_tag(year_str)
        if tag:
            new_image.tags.append(tag)

        try:
            ai_labels = get_ai_tags(save_path) # 调用AI函数
            for label_name in ai_labels:
                ai_tag = get_or_create_tag(label_name)
                if ai_tag and ai_tag not in new_image.tags:
                    new_image.tags.append(ai_tag)
        except Exception as ai_err:
            print(f"AI 识别过程中出错: {ai_err}")

        db.session.commit()
        return True

    except Exception as e:
        print(f"处理失败: {e}")
        db.session.rollback()
        return False

# 使用蓝图来组织路由
bp = Blueprint('main', __name__)

# 首页
@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='首页')

# 登录
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # 尝试按用户名查找用户
        user = User.query.filter_by(username=form.username.data).first()

        # 检查用户名
        if user is None:
            flash('用户名不存在')
            return redirect(url_for('main.login'))

        # 如果用户存在，检查密码
        if not user.check_password(form.password.data):
            flash('密码错误')
            return redirect(url_for('main.login'))

        # 如果两步都通过了，说明登录成功
        login_user(user, remember=form.remember_me.data)
        flash('登录成功！')
        return redirect(url_for('main.dashboard'))
    return render_template('login.html', title='登录', form=form)

# 登出
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# 注册
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜，您已注册成功！')
        return redirect(url_for('main.login'))
        
    return render_template('register.html', title='注册', form=form)

# 仪表盘 (登录后)
@bp.route('/dashboard')
@login_required
def dashboard():
    search_query = request.args.get('q', '').strip() # 获取搜索关键词
    # 基础查询：只查当前用户的图
    query = Image.query.filter_by(user_id=current_user.id)
    if search_query:
        # 构造搜索逻辑
        query = query.outerjoin(Image.tags).filter(
            or_(
                Image.name.contains(search_query),  # 名字包含
                Tag.name.contains(search_query)     # 标签包含
            )
        ).distinct()
    
    # 执行查询 (按上传时间倒序)
    images = query.order_by(Image.uploaded_at.desc()).all()
    
    # 简单的相似度排序优化：Python 层处理
    # 如果有搜索词，让名字里“以关键词开头”的图片排在前面，体验更好
    if search_query:
        images.sort(key=lambda x: 0 if x.name and x.name.startswith(search_query) else 1)

    return render_template('dashboard.html', title='仪表盘', images=images, search_query=search_query) # 把关键词回传给前端显示

@bp.route('/upload', methods=['POST'])
@login_required
def upload_image():
    if 'file' not in request.files:
        flash('没有文件部分')
        return redirect(url_for('main.dashboard'))

    file = request.files['file']

    if file.filename == '':
        flash('未选择文件')
        return redirect(url_for('main.dashboard'))

    # 检查文件类型 
    if file and allowed_file(file.filename):
        success = process_and_save_image(file, current_user.id)
        if success:
            flash('图片上传并处理成功！')
        else:
            flash('图片处理失败。')
    else:
        flash('只允许上传 (png, jpg, jpeg, gif) 格式的图片。')

    return redirect(url_for('main.dashboard'))

@bp.route('/image/delete/<int:image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    image = Image.query.get_or_404(image_id) # 查询图片，如果不存在返回 404
    if image.user_id != current_user.id: # 安全检查：确保只有图片的主人才能删除
        flash('您没有权限删除这张图片。')
        return redirect(url_for('main.dashboard'))
    try:
        # 删除服务器上的物理文件 (原图 + 缩略图)
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename)
        thumb_path = os.path.join(current_app.config['THUMBNAIL_FOLDER'], image.thumbnail)
        # 如果文件存在，就删除
        if os.path.exists(upload_path):
            os.remove(upload_path)
        if os.path.exists(thumb_path):
            os.remove(thumb_path)
        # 删除数据库里的记录
        db.session.delete(image)
        db.session.commit()
        flash('图片已成功删除！')
    except Exception as e:
        db.session.rollback()
        flash(f'删除失败：{str(e)}')
        
    return redirect(url_for('main.dashboard'))

@bp.route('/image/<int:image_id>/tag', methods=['POST'])
@login_required
def add_tag(image_id):
    image = Image.query.get_or_404(image_id) # 获取图片
    if image.user_id != current_user.id: # 权限检查
        abort(403)
    # 获取用户输入的标签名
    tag_name = request.form.get('tag_name')
    if tag_name:
        tag = get_or_create_tag(tag_name)
        if tag and tag not in image.tags:
            image.tags.append(tag)
            db.session.commit()
            flash(f'已添加标签：{tag.name}')
        elif tag in image.tags:
            flash('该标签已存在')

    return redirect(url_for('main.dashboard'))

@bp.route('/image/<int:image_id>/rename', methods=['POST'])
@login_required
def rename_image(image_id):
    # 获取图片
    image = Image.query.get_or_404(image_id)
    
    # 权限检查
    if image.user_id != current_user.id:
        abort(403)
    
    # 获取新名字
    new_name = request.form.get('new_name')
    if new_name:
        image.name = new_name.strip() # 去除首尾空格
        db.session.commit()
        flash('图片名称已修改')
    
    return redirect(url_for('main.dashboard'))

@bp.route('/image/<int:image_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_image(image_id):
    image = Image.query.get_or_404(image_id)
    if image.user_id != current_user.id:
        abort(403)
        
    if request.method == 'POST':
        try:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename)
            img = PILImage.open(file_path)
            
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # 处理旋转
            rotate = request.form.get('rotate', type=int, default=0)
            if rotate != 0:
                img = img.rotate(-rotate, expand=True) 

            # 判断是裁剪还是变形
            active_op = request.form.get('active_op') # 'resize' 或 'crop'
            
            if active_op == 'crop':
                # 执行裁剪
                c_x = request.form.get('crop_x', type=int)
                c_y = request.form.get('crop_y', type=int)
                c_w = request.form.get('crop_width', type=int)
                c_h = request.form.get('crop_height', type=int)
                
                if c_w and c_h and c_w > 0 and c_h > 0:
                    img = img.crop((c_x, c_y, c_x + c_w, c_y + c_h))
            
            elif active_op == 'resize':
                # 执行变形/拉伸
                final_w = request.form.get('final_width', type=int)
                final_h = request.form.get('final_height', type=int)
                
                if final_w and final_h and final_w > 0 and final_h > 0:
                    img = img.resize((final_w, final_h), PILImage.Resampling.LANCZOS)

            # 处理滤镜
            filter_type = request.form.get('filter_type')
            if filter_type == 'gray':
                img = ImageEnhance.Color(img).enhance(0.0)
            elif filter_type == 'contrast':
                img = ImageEnhance.Contrast(img).enhance(1.5)
            elif filter_type == 'bright':
                img = ImageEnhance.Brightness(img).enhance(1.2)

            # 保存
            img.save(file_path, quality=95)
            image.resolution = f"{img.width}x{img.height}"
            
            # 更新缩略图
            thumb_path = os.path.join(current_app.config['THUMBNAIL_FOLDER'], image.thumbnail)
            img.thumbnail((300, 300)) 
            img.save(thumb_path)
            
            db.session.commit()
            flash('图片编辑保存成功！')
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            print(f"处理失败: {e}")
            flash(f'处理失败: {e}')
            return redirect(url_for('main.edit_image', image_id=image.id))
    
    return render_template('edit_image.html', image=image)