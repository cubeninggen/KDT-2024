import os
import torch
import json
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from PIL import Image
import cv2
import numpy as np
from ultralytics import YOLO
from werkzeug.utils import secure_filename
from pathlib import Path
import yaml
import shutil
from datetime import datetime

os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'

app = Flask(__name__)

# YOLO 모델 로드
model = YOLO('yolov5su.pt')

# 결과 저장 폴더 설정
SAVE_FOLDER = './output'
DATASET_FOLDER = './dataset'
TRAIN_FOLDER = os.path.join(DATASET_FOLDER, 'images/train')
LABELS_FOLDER = os.path.join(DATASET_FOLDER, 'labels/train')
MODELS_FOLDER = './models'

# 필요한 디렉토리 생성
for folder in [SAVE_FOLDER, DATASET_FOLDER, TRAIN_FOLDER, LABELS_FOLDER, MODELS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

class DataAugmentation:
    def __init__(self):
        self.augmentations = {
            'rotation': self._rotate_image,
            'flip': self._flip_image,
            'brightness': self._adjust_brightness,
            'noise': self._add_noise
        }

    def _rotate_image(self, image, boxes):
        angle = np.random.uniform(-30, 30)
        height, width = image.shape[:2]
        center = (width/2, height/2)
        
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated_image = cv2.warpAffine(image, M, (width, height))
        
        rotated_boxes = []
        for box in boxes:
            x, y, w, h = box['bbox']
            points = np.array([
                [x, y],
                [x + w, y],
                [x, y + h],
                [x + w, y + h]
            ])
            
            ones = np.ones(shape=(len(points), 1))
            points_ones = np.hstack([points, ones])
            transformed_points = M.dot(points_ones.T).T
            
            x_min = np.clip(np.min(transformed_points[:, 0]), 0, width)
            y_min = np.clip(np.min(transformed_points[:, 1]), 0, height)
            x_max = np.clip(np.max(transformed_points[:, 0]), 0, width)
            y_max = np.clip(np.max(transformed_points[:, 1]), 0, height)
            
            rotated_box = box.copy()
            rotated_box['bbox'] = [x_min, y_min, x_max - x_min, y_max - y_min]
            rotated_boxes.append(rotated_box)
            
        return rotated_image, rotated_boxes

    def _flip_image(self, image, boxes):
        flipped_image = cv2.flip(image, 1)
        width = image.shape[1]
        
        flipped_boxes = []
        for box in boxes:
            x, y, w, h = box['bbox']
            new_x = width - (x + w)
            flipped_box = box.copy()
            flipped_box['bbox'] = [new_x, y, w, h]
            flipped_boxes.append(flipped_box)
            
        return flipped_image, flipped_boxes

    def _adjust_brightness(self, image, boxes):
        value = np.random.uniform(0.7, 1.3)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv = hsv.astype(np.float32)
        hsv[:,:,2] = np.clip(hsv[:,:,2] * value, 0, 255)
        hsv = hsv.astype(np.uint8)
        adjusted_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return adjusted_image, boxes

    def _add_noise(self, image, boxes):
        row, col, ch = image.shape
        mean = 0
        sigma = 25
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        noisy_image = image + gauss
        noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
        return noisy_image, boxes

    def apply_augmentations(self, image, boxes, selected_augmentations):
        augmented_images = []
        augmented_boxes = []
        
        augmented_images.append(image)
        augmented_boxes.append(boxes)
        
        for aug_name in selected_augmentations:
            if aug_name in self.augmentations:
                aug_image, aug_boxes = self.augmentations[aug_name](image.copy(), boxes)
                augmented_images.append(aug_image)
                augmented_boxes.append(aug_boxes)
        
        return augmented_images, augmented_boxes

def prepare_training_data(selected_augmentations=[]):
    augmenter = DataAugmentation()
    json_files = list(Path(SAVE_FOLDER).glob('*_coco.json'))
    
    train_img_dir = os.path.join(DATASET_FOLDER, 'images/train')
    train_label_dir = os.path.join(DATASET_FOLDER, 'labels/train')
    
    for folder in [train_img_dir, train_label_dir]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)
    
    classes = []
    processed_images = 0
    
    for json_file in json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)
            
        image_name = data['images'][0]['file_name']
        src_image = os.path.join(SAVE_FOLDER, image_name)
        
        if os.path.exists(src_image):
            image = cv2.imread(src_image)
            boxes = [{'bbox': ann['bbox'], 'class': ann['class']} 
                    for ann in data['annotations']]
            
            augmented_images, augmented_boxes = augmenter.apply_augmentations(
                image, boxes, selected_augmentations)
            
            for idx, (aug_image, aug_boxes) in enumerate(zip(augmented_images, augmented_boxes)):
                suffix = f"_aug_{idx}" if idx > 0 else ""
                aug_image_name = f"{Path(image_name).stem}{suffix}{Path(image_name).suffix}"
                
                dst_image = os.path.join(train_img_dir, aug_image_name)
                cv2.imwrite(dst_image, aug_image)
                
                label_name = f"{Path(aug_image_name).stem}.txt"
                label_path = os.path.join(train_label_dir, label_name)
                
                img_height, img_width = aug_image.shape[:2]
                
                with open(label_path, 'w') as f:
                    for box in aug_boxes:
                        class_name = box['class']
                        if class_name not in classes:
                            classes.append(class_name)
                        
                        class_id = classes.index(class_name)
                        bbox = box['bbox']
                        
                        x_center = (bbox[0] + bbox[2]/2) / img_width
                        y_center = (bbox[1] + bbox[3]/2) / img_height
                        width = bbox[2] / img_width
                        height = bbox[3] / img_height
                        
                        f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")
                
                processed_images += 1
    
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
        safe_filename = secure_filename(file.filename)
        original_path = os.path.join(SAVE_FOLDER, safe_filename)
        file.save(original_path)

        img = cv2.imread(original_path)
        results = model.predict(source=img, save=False)[0]
        
        detect_image_name = f'result_{safe_filename}'
        detect_path = os.path.join(SAVE_FOLDER, detect_image_name)
        
        plot_image = results.plot()
        cv2.imwrite(detect_path, plot_image)

        json_filename = f"{os.path.splitext(safe_filename)[0]}_detections.json"
        json_path = os.path.join(SAVE_FOLDER, json_filename)
        
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
        
        coco_annotations = {
            "images": [{
                "id": 1,
                "file_name": image_name,
                "width": None,
                "height": None
            }],
            "annotations": []
        }
        
        img_path = os.path.join(SAVE_FOLDER, image_name)
        img = Image.open(img_path)
        img_width, img_height = img.size
        coco_annotations["images"][0]["width"] = img_width
        coco_annotations["images"][0]["height"] = img_height
        
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
        data = request.json
        selected_augmentations = data.get('augmentations', [])
        
        classes = prepare_training_data(selected_augmentations)
        if not classes:
            return jsonify({'error': 'No classes found in the dataset'}), 400
        
        yaml_path = os.path.join(DATASET_FOLDER, 'dataset.yaml')
        config = {
            'path': os.path.abspath(DATASET_FOLDER).replace('\\', '/'),
            'train': 'images/train',
            'val': 'images/train',
            'nc': len(classes),
            'names': classes
        }
        with open(yaml_path, 'w') as f:
            yaml.dump(config, f, sort_keys=False)
        
        train_img_dir = os.path.join(DATASET_FOLDER, 'images/train')
        train_label_dir = os.path.join(DATASET_FOLDER, 'labels/train')
        
        if not os.listdir(train_img_dir) or not os.listdir(train_label_dir):
            return jsonify({'error': 'No training data found'}), 400
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        model_name = f'custom_model_{timestamp}.pt'
        
        training_model = YOLO('yolov8n.pt')
        
        results = training_model.train(
            data=yaml_path,
            epochs=50,
            imgsz=640,
            batch=16,
            device='0' if torch.cuda.is_available() else 'cpu',
            project='runs/train',
            name=model_name.replace('.pt', ''),
            exist_ok=True
        )
        
        model_dir = os.path.join('runs/train', model_name.replace('.pt', ''), 'weights')
        trained_model = os.path.join(model_dir, 'best.pt')
        if not os.path.exists(trained_model):
            trained_model = os.path.join(model_dir, 'last.pt')
        
        new_model_path = os.path.join(MODELS_FOLDER, model_name)
        shutil.copy2(trained_model, new_model_path)
        
        model = YOLO(new_model_path)
        
        return jsonify({
            'message': 'Training completed successfully',
            'model_path': new_model_path,
            'model_name': model_name,
            'classes': classes
        })
        
    except Exception as e:
        print(f"Error during training: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
    
