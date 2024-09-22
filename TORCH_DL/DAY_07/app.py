from flask import Flask, request, jsonify, render_template
import torch
import torch.nn as nn
import torch.nn.functional as F
import os

app = Flask(__name__)

# 모델 클래스 정의
class IrisBCFModel(nn.Module):
    def __init__(self):
        super(IrisBCFModel, self).__init__()
        self.in_layer = nn.Linear(19, 10)
        self.hd_layer1 = nn.Linear(10, 20)
        self.hd_layer2 = nn.Linear(20, 10)
        self.hd_layer3 = nn.Linear(10, 5)
        self.out_layer = nn.Linear(5, 1)

    def forward(self, input_data):
        y = F.relu(self.in_layer(input_data))
        y = F.relu(self.hd_layer1(y))
        y = F.relu(self.hd_layer2(y))
        y = F.relu(self.hd_layer3(y))
        return torch.sigmoid(self.out_layer(y))

# 모델 로드 함수
def load_model():
    model = torch.load('model_R6.pth', map_location=torch.device('cpu'))
    model.eval()  # 평가 모드로 설정
    return model


# 모델 인스턴스 생성 및 로드
model = load_model()

# 예측 함수 정의
def predict(features):
    with torch.no_grad():
        # 입력 데이터를 텐서로 변환
        features_tensor = torch.FloatTensor(features).unsqueeze(0)  # 2D 텐서로 변환
        # 모델에 입력
        output = model(features_tensor)
        return output.item()

# 홈 페이지 라우트
@app.route('/')
def index():
    return render_template('index.html')  # index.html을 렌더링

# 입력 데이터를 받아 예측하는 엔드포인트
@app.route('/predict', methods=['POST'])
def predict_route():
    data = request.json
    features = data.get('features')  # 6개의 입력 피쳐 받아오기
    if features and len(features) == 19:
        prediction = predict(features)
        return jsonify({'prediction': prediction})
    else:
        return jsonify({'error': 'Invalid input'}), 400

if __name__ == '__main__':
    app.run(debug=True)
