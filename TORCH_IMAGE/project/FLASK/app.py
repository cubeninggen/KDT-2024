from flask import Flask, request, jsonify, render_template 
import torch
from torchvision import models, transforms
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 클래스 수 정의 (여기에 오버워치 데이터셋의 클래스 수를 입력)
num_classes = 6  # 클래스 수를 6으로 변경 (이전에 저장된 모델의 클래스 수와 일치)

# 오버워치 모델 불러오기
model = models.resnet50(weights=None)  # 사전 학습된 가중치는 사용하지 않음
num_ftrs = model.fc.in_features
model.fc = torch.nn.Linear(num_ftrs, num_classes)  # 클래스 수에 맞게 마지막 레이어 수정

# 모델 가중치 로드
model.load_state_dict(torch.load('resnet50_OVERWATCH.pth', map_location=torch.device('cpu')))  
model.eval()

# 예측할 캐릭터 이름 리스트 (인덱스와 매핑)
character_names = [
    "D.Va",  # 인덱스 0에 해당하는 캐릭터 이름
    "Genji",  # 인덱스 1에 해당하는 캐릭터 이름
    "Hanzo",  # 인덱스 2에 해당하는 캐릭터 이름
    "Pharah",  # 오타 수정 "Pharah"
    "Roadhog",  # 인덱스 4에 해당하는 캐릭터 이름
    "Tracer"   # 인덱스 5에 해당하는 캐릭터 이름
]

# 이미지 전처리 함수
def transform_image(image_bytes):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # ResNet50의 입력 크기에 맞게 조정
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return transform(image).unsqueeze(0)

# 예측 함수
def get_prediction(image_bytes):
    try:
        tensor = transform_image(image_bytes)
        outputs = model(tensor)
        _, predicted = outputs.max(1)
        return character_names[predicted.item()]  # 예측된 클래스의 이름을 반환
    except Exception as e:
        return str(e)

# 기본 페이지
@app.route('/')
def home():
    return render_template('index.html')  # index.html 파일을 렌더링

# API 엔드포인트
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    img_bytes = file.read()
    predicted_character = get_prediction(img_bytes)
    return jsonify({'character_name': predicted_character})  # 캐릭터 이름을 반환

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
