import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# 初始化插件
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login' # 设置登录页面的端点
login_manager.login_message = '请先登录以访问此页面。' # 设置登录提示信息

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 确保上传和缩略图文件夹存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['THUMBNAIL_FOLDER'], exist_ok=True)

    # 绑定插件到 app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # 注册路由蓝图
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app

from app import models