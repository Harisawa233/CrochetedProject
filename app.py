from flask import Flask, render_template, request, send_file, jsonify, send_from_directory
import os
from PIL import Image, ImageDraw

app = Flask(__name__)

# 配置文件夹路径
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def generate_pattern(input_path, output_path, target_width, target_height):
    """像素化并绘制网格的逻辑"""
    img = Image.open(input_path).convert("RGB")
    
    # 1. 缩放图片到指定的网格大小
    small_img = img.resize((target_width, target_height), resample=Image.NEAREST)
    
    # 2. 放大以供展示（每个格子放大为 30x30 像素）
    pixel_size = 30
    final_img = small_img.resize((target_width * pixel_size, target_height * pixel_size), resample=Image.NEAREST)
    
    # 3. 绘制网格线
    draw = ImageDraw.Draw(final_img)
    
    # 画竖线
    for x in range(0, target_width * pixel_size + 1, pixel_size):
        draw.line([(x, 0), (x, target_height * pixel_size)], fill="black", width=1)
    
    # 画横线
    for y in range(0, target_height * pixel_size + 1, pixel_size):
        draw.line([(0, y), (target_width * pixel_size, y)], fill="black", width=1)
        
    final_img.save(output_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 接收上传的图片
        file = request.files['file']
        width = int(request.form['width'])
        height = int(request.form['height'])
        
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        # 定义输出文件名
        output_filename = "pattern.jpg"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        
        # 执行逻辑
        generate_pattern(file_path, output_path, width, height)
        
        # 返回 JSON 给前端
        return jsonify({'image_url': f'/uploads/{output_filename}'})
    
    return render_template('index.html')

@app.route('/get_ratio', methods=['POST'])
def get_ratio():
    file = request.files['file']
    img = Image.open(file)
    w, h = img.size
    # 默认宽度为 50，自动计算高度
    suggested_width = 50
    suggested_height = int(50 * (h / w))
    return jsonify({'width': suggested_width, 'height': suggested_height})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """允许前端访问生成的图片"""
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    # 将 host 设置为 '0.0.0.0'
    app.run(host='0.0.0.0', port=5000)