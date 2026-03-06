# 使用轻量级 Python 镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制整个项目到容器中
COPY . .

# 确保上传目录存在
RUN mkdir -p app/static/uploads app/static/thumbnails

# 设置环境变量
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# 暴露端口
EXPOSE 5000

# 使用 Gunicorn 启动应用
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]