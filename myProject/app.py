from flask import Flask, Response, render_template
import cv2
import torch
from torchvision import models, transforms
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 클래스 수 정의
num_classes = 6  # 클래스 수를 6으로 변경

# 오버워치 모델 불러오기
model = models.resnet50(weights=None)  # 사전 학습된 가중치는 사용하지 않음
num_ftrs = model.fc.in_features
model.fc = torch.nn.Linear(num_ftrs, num_classes)  # 클래스 수에 맞게 마지막 레이어 수정

# 모델 가중치 로드
model.load_state_dict(torch.load('resnet50_OVERWATCH.pth', map_location=torch.device('cpu')))
model.eval()

# 예측할 캐릭터 이름 리스트 (인덱스와 매핑)
character_names = [
    "D.Va",
    "Genji",
    "Hanzo",
    "Pharah",
    "Roadhog",
    "Tracer"
]

# 이미지 전처리 함수
def transform_image(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # ResNet50의 입력 크기에 맞게 조정
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0)

# 예측 함수
def get_prediction(image):
    tensor = transform_image(image)
    outputs = model(tensor)
    _, predicted = outputs.max(1)
    
    # 예측된 값이 character_names의 범위 내에 있을 때 해당 이름을 반환, 그렇지 않으면 "None" 반환
    if 0 <= predicted.item() < len(character_names):
        return character_names[predicted.item()]
    else:
        return "None"

# VideoCapture 객체 생성
video_source = 0  # 0은 기본 웹캠
cap = cv2.VideoCapture(video_source)

def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        # OpenCV BGR to PIL RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image)

        # 예측
        predicted_character = get_prediction(pil_image)

        # 프레임에 예측 결과 표시
        cv2.putText(frame, f'Predicted: {predicted_character}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # JPEG로 인코딩
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def home():
    return render_template('index.html')  # index.html 파일을 렌더링

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
