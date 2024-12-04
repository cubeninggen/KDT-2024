import os
import torch
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image
import cv2
import numpy as np
from ultralytics import YOLO
from werkzeug.utils import secure_filename
from pathlib import Path
import yaml
import shutil
from datetime import datetime

import os
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'

app = Flask(__name__)

# YOLO 모델 로드
model = YOLO('yolov5su.pt')  # YOLOv5 사용

# 결과 저장 폴더 설정
SAVE_FOLDER = './output'
DATASET_FOLDER = './dataset'
TRAIN_FOLDER = os.path.join(DATASET_FOLDER, 'images/train')
LABELS_FOLDER = os.path.join(DATASET_FOLDER, 'labels/train')
MODELS_FOLDER = './models'

# 필요한 디렉토리 생성
for folder in [SAVE_FOLDER, DATASET_FOLDER, TRAIN_FOLDER, LABELS_FOLDER, MODELS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

print("Training folder contents:", os.listdir(TRAIN_FOLDER))
print("Labels folder contents:", os.listdir(LABELS_FOLDER))

def convert_coco_to_yolo(json_data, img_path):
    """COCO 형식의 어노테이션을 YOLO 형식으로 변환"""
    img = Image.open(img_path)
    img_width, img_height = img.size
    
    yolo_annotations = []
    
    for ann in json_data['annotations']:
        bbox = ann['bbox']  # [x, y, width, height]
        class_name = ann['class']
        
        # YOLO 형식으로 변환 (x_center, y_center, width, height)
        x_center = (bbox[0] + bbox[2]/2) / img_width
        y_center = (bbox[1] + bbox[3]/2) / img_height
        width = bbox[2] / img_width
        height = bbox[3] / img_height
        
        yolo_annotations.append(f"{class_name} {x_center} {y_center} {width} {height}")
    
    return yolo_annotations

def create_yaml_config(classes):
    """YOLO 학습을 위한 YAML 설정 파일 생성"""
    yaml_path = os.path.join(DATASET_FOLDER, 'dataset.yaml')
    
    # 경로를 올바르게 설정 (윈도우 경로 이슈 해결)
    dataset_path = os.path.abspath(DATASET_FOLDER).replace('\\', '/')
    train_path = os.path.join(dataset_path, 'images/train').replace('\\', '/')
    
    config = {
        'path': dataset_path,  # 메인 데이터셋 경로
        'train': 'images/train',  # 상대 경로 사용
        'val': 'images/train',    # 상대 경로 사용
        'nc': len(classes),       # 클래스 수
        'names': classes          # 클래스 이름 리스트
    }
    
    print("Creating YAML with config:", config)  # 디버깅용
    
    with open(yaml_path, 'w') as f:
        yaml.dump(config, f, sort_keys=False)
    
    return yaml_path

def prepare_training_data():
    """학습 데이터 준비"""
    print("Starting prepare_training_data")  # 디버깅용
    
    json_files = list(Path(SAVE_FOLDER).glob('*_coco.json'))
    print(f"Found {len(json_files)} JSON files")  # 디버깅용
    
    # 디렉토리 재생성
    train_img_dir = os.path.join(DATASET_FOLDER, 'images/train')
    train_label_dir = os.path.join(DATASET_FOLDER, 'labels/train')
    
    for folder in [train_img_dir, train_label_dir]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)
    
    classes = []
    processed_images = 0
    
    for json_file in json_files:
        print(f"Processing {json_file}")  # 디버깅용
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # 이미지 파일 복사
        image_name = data['images'][0]['file_name']
        src_image = os.path.join(SAVE_FOLDER, image_name)
        if os.path.exists(src_image):
            dst_image = os.path.join(train_img_dir, image_name)
            shutil.copy2(src_image, dst_image)
            print(f"Copied image to {dst_image}")  # 디버깅용
            
            # YOLO 형식으로 레이블 변환
            img_width = float(data['images'][0]['width'])
            img_height = float(data['images'][0]['height'])
            
            label_name = Path(image_name).stem + '.txt'
            label_path = os.path.join(train_label_dir, label_name)
            
            with open(label_path, 'w') as f:
                for ann in data['annotations']:
                    class_name = ann['class']
                    if class_name not in classes:
                        classes.append(class_name)
                    
                    class_id = classes.index(class_name)
                    bbox = ann['bbox']  # [x, y, width, height]
                    x_center = (bbox[0] + bbox[2]/2) / img_width
                    y_center = (bbox[1] + bbox[3]/2) / img_height
                    width = bbox[2] / img_width
                    height = bbox[3] / img_height
                    
                    f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")
            print(f"Created label file {label_path}")  # 디버깅용
            processed_images += 1
        else:
            print(f"Warning: Image {src_image} not found")  # 디버깅용
    
    print(f"Processed {processed_images} images with classes: {classes}")  # 디버깅용
    
    # 데이터셋 구조 확인
    print("Dataset structure:")
    print(f"Train images: {os.listdir(train_img_dir)}")
    print(f"Train labels: {os.listdir(train_label_dir)}")
    
    return classes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # 파일명에서 특수문자 제거 및 안전한 파일명 생성
        safe_filename = secure_filename(file.filename)
        original_path = os.path.join(SAVE_FOLDER, safe_filename)
        file.save(original_path)

        # 이미지 읽기
        img = cv2.imread(original_path)
        
        # YOLO 객체 탐지 실행
        results = model.predict(source=img, save=False)[0]
        
        # 결과 이미지 이름 설정
        detect_image_name = f'result_{safe_filename}'
        detect_path = os.path.join(SAVE_FOLDER, detect_image_name)
        
        # 결과 이미지에 바운딩 박스 그리기
        plot_image = results.plot()
        cv2.imwrite(detect_path, plot_image)

        # JSON 결과 저장
        json_filename = f"{os.path.splitext(safe_filename)[0]}_detections.json"
        json_path = os.path.join(SAVE_FOLDER, json_filename)
        
        # 탐지 결과를 JSON으로 변환
        detections = []
        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            conf = float(box.conf[0].cpu().numpy())
            cls = int(box.cls[0].cpu().numpy())
            name = results.names[cls]
            
            detection = {
                "class": name,
                "confidence": conf,
                "bbox": [float(x1), float(y1), float(x2-x1), float(y2-y1)]
            }
            detections.append(detection)

        with open(json_path, 'w') as f:
            json.dump(detections, f, indent=4)

        return jsonify({
            'original_image': f'/output/{safe_filename}',
            'result_image': f'/output/{detect_image_name}',
            'json_file': f'/output/{json_filename}',
            'message': 'Processing completed successfully'
        })

    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/output/<path:filename>')
def output_files(filename):
    try:
        return send_from_directory(SAVE_FOLDER, filename)
    except Exception as e:
        print(f"Error serving file {filename}: {str(e)}")
        return jsonify({'error': 'File not found'}), 404

@app.route('/save_labels', methods=['POST'])
def save_labels():
    try:
        data = request.json
        image_name = data['image_name']
        bboxes = data['bboxes']
        
        # COCO 형식으로 저장
        coco_annotations = {
            "images": [{
                "id": 1,
                "file_name": image_name,
                "width": None,
                "height": None
            }],
            "annotations": []
        }
        
        # 이미지 크기 가져오기
        img_path = os.path.join(SAVE_FOLDER, image_name)
        img = Image.open(img_path)
        img_width, img_height = img.size
        coco_annotations["images"][0]["width"] = img_width
        coco_annotations["images"][0]["height"] = img_height
        
        # 바운딩 박스를 COCO 형식으로 변환
        for i, bbox in enumerate(bboxes):
            x_center = bbox['x_center'] * img_width
            y_center = bbox['y_center'] * img_height
            width = bbox['width'] * img_width
            height = bbox['height'] * img_height
            
            x = x_center - (width / 2)
            y = y_center - (height / 2)
            
            coco_annotations["annotations"].append({
                "id": i + 1,
                "image_id": 1,
                "class": bbox['class'],
                "bbox": [x, y, width, height],
                "area": width * height,
                "iscrowd": 0
            })
        
        # COCO JSON 저장
        json_path = os.path.join(SAVE_FOLDER, f"{os.path.splitext(image_name)[0]}_coco.json")
        with open(json_path, 'w') as f:
            json.dump(coco_annotations, f, indent=4)
        
        return jsonify({
            "message": "Labels saved successfully",
            "coco_file": json_path
        })
    
    except Exception as e:
        print(f"Error saving labels: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/delete_image', methods=['POST'])
def delete_image():
    try:
        data = request.json
        filename = data.get('filename')
        if not filename:
            return jsonify({'error': 'No filename provided'}), 400

        # 관련된 모든 파일 삭제
        base_name = os.path.splitext(filename)[0]
        files_to_delete = [
            filename,
            f'result_{filename}',
            f'{base_name}_detections.json',
            f'{base_name}_coco.json'
        ]

        for file in files_to_delete:
            file_path = os.path.join(SAVE_FOLDER, file)
            if os.path.exists(file_path):
                os.remove(file_path)

        return jsonify({'message': 'Files deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/train', methods=['POST'])
def train_model():
    try:
        global model
        
        # 학습 데이터 준비
        classes = prepare_training_data()
        if not classes:
            return jsonify({'error': 'No classes found in the dataset'}), 400
        
        yaml_path = create_yaml_config(classes)
        
        # 학습 데이터 존재 확인
        train_img_dir = os.path.join(DATASET_FOLDER, 'images/train')
        train_label_dir = os.path.join(DATASET_FOLDER, 'labels/train')
        
        if not os.listdir(train_img_dir) or not os.listdir(train_label_dir):
            return jsonify({'error': 'No training data found'}), 400
        
        # 현재 시간으로 모델 이름 생성
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        model_name = f'custom_model_{timestamp}'
        
        # YOLO 모델 학습 설정
        training_model = YOLO('yolov8n.pt')
        
        print(f"Starting training with YAML config at {yaml_path}")
        
        # 학습 실행
        results = training_model.train(
            data=yaml_path,
            epochs=50,
            imgsz=640,
            batch=16,
            device='0' if torch.cuda.is_available() else 'cpu',
            project='runs/train',
            name=model_name,
            exist_ok=True
        )
        
        # 학습된 모델 파일 경로 찾기
        model_dir = os.path.join('runs/train', model_name, 'weights')
        trained_model = os.path.join(model_dir, 'best.pt')
        if not os.path.exists(trained_model):
            trained_model = os.path.join(model_dir, 'last.pt')
        
        # 모델 파일 이동
        new_model_path = os.path.join(MODELS_FOLDER, f'{model_name}.pt')
        shutil.copy2(trained_model, new_model_path)
        
        # 글로벌 모델 업데이트
        model = YOLO(new_model_path)
        
        return jsonify({
            'message': 'Training completed successfully',
            'model_path': new_model_path,
            'classes': classes
        })
        
    except Exception as e:
        print(f"Error during training: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)