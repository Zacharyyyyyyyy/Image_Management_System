from app import create_app, db
from app.models import User, Image, Tag

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """为 'flask shell' 命令提供上下文，方便调试"""
    return {'db': db, 'User': User, 'Image': Image, 'Tag': Tag}

# 自动创建数据库表
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    # 允许直接运行 python run.py 进行本地调试
    app.run(host='0.0.0.0', port=5000)