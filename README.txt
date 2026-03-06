如何运行项目

1. 设置数据库：
   - 确保您已安装并启动 MySQL。
   - 登录 MySQL，创建一个新数据库：
     CREATE DATABASE imagedb;
   - 【重要】：打开 config.py 文件，修改 SQLALCHEMY_DATABASE_URI，将 "root:000000" 替换为您自己的 MySQL 用户名和密码。

2. 创建虚拟环境 (在 ImageManager 根目录执行)：
   # Windows:
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate

3. 安装依赖：
   pip install -r requirements.txt

4. 初始化数据库 (关键步骤)：
   # 注意：请使用 'python -m flask' 命令以确保兼容性

   # 设置 FLASK_APP 环境变量
   # (Windows PowerShell)
   $env:FLASK_APP = "run.py"
   # (Windows CMD)
   set FLASK_APP=run.py
   # (macOS/Linux)
   export FLASK_APP=run.py

   # 依次执行以下命令：
   # 1. 初始化迁移文件夹 (如果 migrations 文件夹不存在)
   python -m flask db init
   
   # 2. 生成迁移脚本 (这会自动检测 User, Image 和 Tag 表)
   python -m flask db migrate -m "Initial database setup"
   
   # 3. 应用更改到数据库 (创建表)
   python -m flask db upgrade

   # (如果一切顺利，您将在 MySQL imagedb 数据库中看到 user, image, tag 等表)

5. 运行应用：
   python -m flask run

6. 访问网站：
   在浏览器中打开 http://127.0.0.1:5000。