from flask import Flask, request, render_template
import torch
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)

# 모델과 벡터라이저 로드
class YourModel(torch.nn.Module):
    def __init__(self, input_size, output_size):
        super(YourModel, self).__init__()
        self.fc1 = torch.nn.Linear(input_size, 50)
        self.fc2 = torch.nn.Linear(50, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 모델 초기화
input_size = 14009  # 벡터라이저에서 나온 특징 수에 맞춰 조정
output_size = 1
model = YourModel(input_size, output_size)
model.load_state_dict(torch.load('overwatch_model.pth', map_location=torch.device('cpu')))
model.eval()

# TF-IDF 벡터라이저 로드
with open('tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        new_comment = request.form['comment']
        # 벡터화
        comment_vector = vectorizer.transform([new_comment])
        comment_tensor = torch.tensor(comment_vector.toarray(), dtype=torch.float32)
        
        # 예측
        with torch.no_grad():
            prediction = model(comment_tensor).item()
        
        # 이진 분류 결과 변환
        prediction = "Overwatch 관련" if prediction >= 0.5 else "비관련"

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
