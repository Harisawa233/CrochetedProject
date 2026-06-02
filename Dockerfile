# 使用轻量级 Python 镜像
FROM python:3.11-slim

# 设置容器内的工作目录
WORKDIR /app

# 将当前目录下的所有文件复制到容器的 /app 目录
COPY . .

# 安装依赖项（包括 gunicorn，它是生产环境的推荐服务器）
RUN pip install --no-cache-dir Flask Pillow gunicorn

# 暴露端口（虽然 Render 会动态分配，但声明一下是好习惯）
EXPOSE 5000

# 使用 gunicorn 启动应用
# -b 0.0.0.0:5000: 绑定到所有网络接口
# app:app: 指的是 app.py 文件中的 app 对象
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]