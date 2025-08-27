# 使用官方 Python 基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制整个项目代码到容器内
COPY . .

# 设置环境变量（可选）
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# 暴露 Flask 默认端口
EXPOSE 5000

# 启动应用
CMD ["python", "app.py"]