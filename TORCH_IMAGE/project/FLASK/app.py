from flask import Flask, request, jsonify
import torch
from torchvision import models, transforms
from PIL import Image
import io
from flask_cors import CORS  # CORS 문제 해결을 위해 추가

app = Flask(__name__)
CORS(app)  # CORS 설정 (서버-클라이언트 간의 도메인 차이 문제 해결)

# VGG16 모델 불러오기 (CIFAR-10에 맞춰 수정된 모델)
vgg16 = models.vgg16(pretrained=True)
vgg16.classifier[6] = torch.nn.Linear(4096, 10)  # CIFAR-10 클래스 수에 맞게 마지막 레이어 수정
vgg16.eval()

# CIFAR-10 클래스 레이블
CIFAR_CLASSES = [
    "Airplane", "Automobile", "Bird", "Cat", "Deer",
    "Dog", "Frog", "Horse", "Ship", "Truck"
]

# 이미지 전처리 함수 (CIFAR-10과 맞는 크기와 정규화 사용)
def transform_image(image_bytes):
    transform = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    image = Image.open(io.BytesIO(image_bytes))
    return transform(image).unsqueeze(0)  # 배치 차원 추가

# 예측 함수
def get_prediction(image_bytes):
    tensor = transform_image(image_bytes)
    outputs = vgg16(tensor)
    _, predicted = outputs.max(1)  # 가장 높은 값을 가진 클래스 예측
    return CIFAR_CLASSES[predicted.item()]

# API 엔드포인트: 이미지를 받아 예측 결과 반환
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    img_bytes = file.read()
    class_name = get_prediction(img_bytes)
    return jsonify({'class_name': class_name})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Flask 서버를 모든 네트워크 인터페이스에서 접근 가능하게 설정
