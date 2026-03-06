import os

# 获取项目根目录的绝对路径，确保数据库文件位置固定
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # 保持密钥安全，不要硬编码
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-hard-to-guess-secret-key'
    
    # SQLite 数据库配置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 图片上传配置（建议优先从环境变量读取，以适配 Docker 配置）
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'app/static/uploads'
    THUMBNAIL_FOLDER = os.environ.get('THUMBNAIL_FOLDER') or 'app/static/thumbnails'