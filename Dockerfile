# 1. 使用轻量级的 Python 作为基础镜像
FROM python:3.11-slim

# 2. 设置工作目录
WORKDIR /app

# 3. 复制你的代码进去
COPY . .

# 4. 安装依赖
RUN pip install Flask Pillow

# 5. 开放 5000 端口
EXPOSE 5000

# 6. 运行程序
CMD ["python", "app.py"]