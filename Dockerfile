# 使用官方 Python 运行时作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录下的 requirements.txt 文件到容器中的 /app 目录
COPY requirements.txt .

# 安装应用所需依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码到容器
COPY . .

# 创建用于存储 SQLite 数据库的目录
RUN mkdir -p /app/data

# 设置环境变量（可选）
# ENV FLASK_APP=app.py
# ENV FLASK_ENV=production

# 暴露 5000 端口，Flask 默认运行在此端口
EXPOSE 5000

# 创建非 root 用户以提高安全性
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# 定义运行容器时执行的命令
CMD ["python", "app.py"]
