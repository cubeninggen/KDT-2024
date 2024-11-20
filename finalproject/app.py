from flask import Flask, render_template, request, jsonify
import os
from PIL import Image, ImageDraw

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
LABELED_FOLDER = 'static/labeled'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(LABELED_FOLDER, exist_ok=True)

label_data = {}  # 이미지별 라벨 데이터 저장

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_images():
    uploaded_files = request.files.getlist('images')
    filepaths = []

    for file in uploaded_files:
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            filepaths.append(filepath)
            label_data[filepath] = []  # 초기화

    return jsonify({'filepaths': filepaths})

@app.route('/save_label', methods=['POST'])
def save_label():
    data = request.json
    filepath = data.get('filepath')
    rectangles = data.get('rectangles')

    if not filepath or not rectangles:
        return jsonify({'error': 'Invalid data'}), 400

    img = Image.open(filepath)
    draw = ImageDraw.Draw(img)

    for rect in rectangles:
        x1, y1, x2, y2 = rect
        draw.rectangle([x1, y1, x2, y2], outline='red', width=2)

    labeled_path = os.path.join(LABELED_FOLDER, os.path.basename(filepath))
    img.save(labeled_path)

    return jsonify({'message': 'Label saved successfully', 'labeled_filepath': labeled_path})

@app.route('/save_all', methods=['POST'])
def save_all():
    data = request.json
    all_label_data = data.get('all_label_data', {})

    for filepath, rectangles in all_label_data.items():
        if not rectangles:
            continue

        img = Image.open(filepath)
        draw = ImageDraw.Draw(img)

        for rect in rectangles:
            x1, y1, x2, y2 = rect
            draw.rectangle([x1, y1, x2, y2], outline='red', width=2)

        labeled_path = os.path.join(LABELED_FOLDER, os.path.basename(filepath))
        img.save(labeled_path)

    return jsonify({'message': 'All images saved successfully'})

if __name__ == '__main__':
    app.run(debug=True)
