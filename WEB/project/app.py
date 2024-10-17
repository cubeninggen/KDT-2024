from flask import Flask, request, jsonify, render_template
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
import io
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 1. 모델 1: IrisBCFModel 정의
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

# 모델 1 로드 함수
def load_iris_model():
    model = torch.load('model_R6.pth', map_location=torch.device('cpu'))
    model.eval()
    return model

iris_model = load_iris_model()

# 예측 함수 1
def predict_iris(features):
    with torch.no_grad():
        features_tensor = torch.FloatTensor(features).unsqueeze(0)
        output = iris_model(features_tensor)
        return output.item()

# 2. 모델 2: ResNet50 for Overwatch character classification
num_classes = 6
resnet_model = models.resnet50(weights=None)
num_ftrs = resnet_model.fc.in_features
resnet_model.fc = nn.Linear(num_ftrs, num_classes)
resnet_model.load_state_dict(torch.load('resnet50_OVERWATCH.pth', map_location=torch.device('cpu')))
resnet_model.eval()

character_names = ["D.Va", "Genji", "Hanzo", "Pharah", "Roadhog", "Tracer"]

# 이미지 전처리
def transform_image(image_bytes):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return transform(image).unsqueeze(0)

# 예측 함수 2
def get_resnet_prediction(image_bytes):
    try:
        tensor = transform_image(image_bytes)
        outputs = resnet_model(tensor)
        _, predicted = outputs.max(1)
        return character_names[predicted.item()]
    except Exception as e:
        return str(e)

# 3. 모델 3: TF-IDF와 Overwatch 관련 예측 모델
class YourModel(nn.Module):
    def __init__(self, input_size, output_size):
        super(YourModel, self).__init__()
        self.fc1 = nn.Linear(input_size, 50)
        self.fc2 = nn.Linear(50, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

input_size = 14009
output_size = 1
comment_model = YourModel(input_size, output_size)
comment_model.load_state_dict(torch.load('overwatch_model.pth', map_location=torch.device('cpu')))
comment_model.eval()

with open('tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# 예측 함수 3
def predict_comment(new_comment):
    comment_vector = vectorizer.transform([new_comment])
    comment_tensor = torch.tensor(comment_vector.toarray(), dtype=torch.float32)
    with torch.no_grad():
        prediction = comment_model(comment_tensor).item()
    return "Overwatch 관련" if prediction >= 0.5 else "비관련"

# Routes

# 홈 페이지 라우트
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_iris_temp')
def predict_iris_temp():
    return render_template('predict_iris.html')

@app.route('/predict_image_temp')
def predict_image_temp():
    return render_template('predict_image.html')

@app.route('/predict_comment_temp')
def predict_comment_temp():
    return render_template('predict_comment.html')

# IrisBCFModel 예측 엔드포인트
@app.route('/predict_iris', methods=['POST'])
def predict_iris_route():
    data = request.json
    features = data.get('features')
    if features and len(features) == 19:
        prediction = predict_iris(features)
        return jsonify({'prediction': prediction})
    else:
        return jsonify({'error': 'Invalid input'}), 400

# ResNet50 예측 엔드포인트
@app.route('/predict_image', methods=['POST'])
def predict_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    img_bytes = file.read()
    predicted_character = get_resnet_prediction(img_bytes)
    return jsonify({'character_name': predicted_character})

# 댓글 예측 엔드포인트
@app.route('/predict_comment', methods=['POST'])
def predict_comment_route():
    new_comment = request.form['comment']
    prediction = predict_comment(new_comment)
    return render_template('predict_comment.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
