import os
import torch
import json
import queue
import threading
from flask import Flask, render_template, request, jsonify, Response, stream_with_context, send_from_directory
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

# 훈련 상태를 저장할 전역 큐와 현재 훈련 경로
training_updates = queue.Queue()
current_training_path = None

class TrainingCallback:
    def on_train_batch_end(self, trainer):
        try:
            metrics = trainer.label_loss_items(trainer.tloss, prefix="train")
            memory_used = torch.cuda.memory_reserved() // 1E9 if torch.cuda.is_available() else 0
            
            if isinstance(metrics, dict):
                update = {
                    "currentEpoch": trainer.epoch,
                    "totalEpochs": trainer.epochs,
                    "box_loss": float(metrics.get('box_loss', 0)),
                    "cls_loss": float(metrics.get('cls_loss', 0)),
                    "dfl_loss": float(metrics.get('dfl_loss', 0)),
                    "gpu_memory": f"{memory_used:.1f}G" if memory_used > 0 else "CPU",
                    "instances": len(trainer.train_loader.dataset),
                    "batch_size": trainer.batch_size,
                    "training_path": current_training_path
                }
            else:
                update = {
                    "currentEpoch": trainer.epoch,
                    "totalEpochs": trainer.epochs,
                    "box_loss": float(metrics[0]) if len(metrics) > 0 else 0,
                    "cls_loss": float(metrics[1]) if len(metrics) > 1 else 0,
                    "dfl_loss": float(metrics[2]) if len(metrics) > 2 else 0,
                    "gpu_memory": f"{memory_used:.1f}G" if memory_used > 0 else "CPU",
                    "instances": len(trainer.train_loader.dataset),
                    "batch_size": trainer.batch_size,
                    "training_path": current_training_path
                }
            
            training_updates.put(json.dumps(update))
            
        except Exception as e:
            print(f"Error in on_train_batch_end: {str(e)}")
            update = {
                "currentEpoch": trainer.epoch,
                "totalEpochs": trainer.epochs,
                "box_loss": 0,
                "cls_loss": 0,
                "dfl_loss": 0,
                "gpu_memory": "CPU",
                "instances": 0,
                "batch_size": trainer.batch_size,
                "training_path": current_training_path
            }
            training_updates.put(json.dumps(update))

    def on_train_end(self, trainer):
        try:
            model_summary = {
                "parameters": sum(p.numel() for p in trainer.model.parameters()),
                "gradients": sum(p.numel() for p in trainer.model.parameters() if p.requires_grad),
                "layers": len(list(trainer.model.modules())),
                "gflops": trainer.model.flops / 1E9 if hasattr(trainer.model, 'flops') else 0
            }
            
            update = {
                "training_path": current_training_path,
                "modelSummary": model_summary,
                "training_complete": True
            }
            training_updates.put(json.dumps(update))
            
        except Exception as e:
            print(f"Error in on_train_end: {str(e)}")
            update = {
                "training_path": current_training_path,
                "modelSummary": {
                    "parameters": 0,
                    "layers": 0,
                    "gradients": 0,
                    "gflops": 0
                },
                "training_complete": True
            }
            training_updates.put(json.dumps(update))
class DataAugmentation:
    def __init__(self):
        self.augmentations = {
            'rotation': self._rotate_image,
            'flip': self._flip_image,
            'brightness': self._adjust_brightness,
            'noise': self._add_noise
        }

    def _rotate_image(self, image, boxes, angle_range=30):
        angle = np.random.uniform(-angle_range, angle_range)
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

    def _adjust_brightness(self, image, boxes, factor_range=0.3):
        factor = np.random.uniform(1 - factor_range, 1 + factor_range)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv = hsv.astype(np.float32)
        hsv[:,:,2] = np.clip(hsv[:,:,2] * factor, 0, 255)
        hsv = hsv.astype(np.uint8)
        adjusted_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return adjusted_image, boxes

    def _add_noise(self, image, boxes, sigma=25):
        noise = np.random.normal(0, sigma, image.shape).astype(np.float32)
        noisy_image = cv2.add(image.astype(np.float32), noise)
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
    
    for folder in [TRAIN_FOLDER, LABELS_FOLDER]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)
    
    classes = set()
    
    for json_file in json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)
            
        image_name = data['images'][0]['file_name']
        image_path = os.path.join(SAVE_FOLDER, image_name)
        
        if os.path.exists(image_path):
            image = cv2.imread(image_path)
            boxes = [{
                'bbox': ann['bbox'],
                'class': ann['class']
            } for ann in data['annotations']]
            
            augmented_images, augmented_boxes = augmenter.apply_augmentations(
                image, boxes, selected_augmentations)
            
            for idx, (aug_image, aug_boxes) in enumerate(zip(augmented_images, augmented_boxes)):
                suffix = f"_aug_{idx}" if idx > 0 else ""
                aug_image_name = f"{Path(image_name).stem}{suffix}{Path(image_name).suffix}"
                
                cv2.imwrite(os.path.join(TRAIN_FOLDER, aug_image_name), aug_image)
                
                label_name = f"{Path(aug_image_name).stem}.txt"
                label_path = os.path.join(LABELS_FOLDER, label_name)
                
                height, width = aug_image.shape[:2]
                with open(label_path, 'w') as f:
                    for box in aug_boxes:
                        class_name = box['class']
                        classes.add(class_name)
                        
                        bbox = box['bbox']
                        x_center = (bbox[0] + bbox[2]/2) / width
                        y_center = (bbox[1] + bbox[3]/2) / height
                        box_width = bbox[2] / width
                        box_height = bbox[3] / height
                        
                        class_idx = len(classes) - 1
                        f.write(f"{class_idx} {x_center} {y_center} {box_width} {box_height}\n")
    
    return sorted(list(classes))
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    def generate():
        while True:
            try:
                update = training_updates.get(timeout=1.0)
                yield f"data: {update}\n\n"
            except queue.Empty:
                yield f"data: {json.dumps({'heartbeat': True})}\n\n"

    return Response(stream_with_context(generate()), 
                   mimetype='text/event-stream')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(SAVE_FOLDER, filename)
        file.save(filepath)

        results = model(filepath)[0]
        result_path = os.path.join(SAVE_FOLDER, f'result_{filename}')
        results.save(result_path)

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

        json_path = os.path.join(SAVE_FOLDER, f'{Path(filename).stem}_detections.json')
        with open(json_path, 'w') as f:
            json.dump(detections, f, indent=4)

        return jsonify({
            'original_image': f'/output/{filename}',
            'result_image': f'/output/result_{filename}',
            'json_file': f'/output/{Path(filename).stem}_detections.json',
            'message': 'Processing completed successfully'
        })

    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/output/<path:filename>')
def output_files(filename):
    return send_from_directory(SAVE_FOLDER, filename)

@app.route('/training_results/<path:filename>')
def training_results(filename):
    if current_training_path and os.path.exists(current_training_path):
        return send_from_directory(current_training_path, filename)
    return jsonify({'error': 'Training results not found'}), 404

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

@app.route('/train', methods=['POST'])
def train_model():
    try:
        data = request.json
        selected_augmentations = data.get('augmentations', [])
        
        callback = TrainingCallback()
        classes = prepare_training_data(selected_augmentations)
        
        if not classes:
            raise ValueError('No classes found in the dataset')
        
        yaml_path = os.path.join(DATASET_FOLDER, 'dataset.yaml')
        config = {
            'path': os.path.abspath(DATASET_FOLDER),
            'train': 'images/train',
            'val': 'images/train',
            'nc': len(classes),
            'names': classes
        }
        with open(yaml_path, 'w') as f:
            yaml.dump(config, f, sort_keys=False)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        model_name = f'custom_model_{timestamp}'
        
        global current_training_path
        current_training_path = os.path.join('runs/train', model_name)
        
        def train_thread():
            training_model = YOLO('yolov8n.pt')
            training_model.add_callback("on_train_batch_end", callback.on_train_batch_end)
            training_model.add_callback("on_train_end", callback.on_train_end)
            
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
            
            model_dir = os.path.join('runs/train', model_name, 'weights')
            best_model = os.path.join(model_dir, 'best.pt')
            if not os.path.exists(best_model):
                best_model = os.path.join(model_dir, 'last.pt')
            
            new_model_path = os.path.join(MODELS_FOLDER, f'{model_name}.pt')
            shutil.copy2(best_model, new_model_path)
            
            global model
            model = YOLO(new_model_path)

        threading.Thread(target=train_thread).start()
        
        return jsonify({
            'message': 'Training started successfully',
            'model_name': model_name,
            'training_path': current_training_path
        })
        
    except Exception as e:
        print(f"Error during training: {str(e)}")
        import traceback
        traceback.print_exc()
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)