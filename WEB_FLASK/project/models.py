#--------------------------------------------------------------------------------------
# 데이터 베이스의 테이블 정의 클래스
# -------------------------------------------------------------------------------------- 
# 모듈로딩

# from PROWEB import DB

import torch.nn as nn


#---------------------------------------------------------------------------------------
# Result
#---------------------------------------------------------------------------------------
# class Result(DB.Model):
#     # 컬럼정의
#     hum=DB.Column(DB.Integer,nullable=False)
#     rain=DB.Column(DB.Integet,nullable=False)
#     tem=DB.Column(DB.float,nullable=False)
#     wind=DB.Column(DB.float,nullable=False)


class IrisRegModel(nn.Module):
    def __init__(self):
        super().__init__()
        # 1. 입력층 4 -> 16
        self.in_layer = nn.Linear(4, 16)
        
        # 2~10. 은닉층 (LeakyReLU 포함)
        self.hd_layer1 = nn.Linear(16, 32)
        self.hd_layer2 = nn.Linear(32, 64)
        self.hd_layer3 = nn.Linear(64, 128)
        self.hd_layer4 = nn.Linear(128, 64)
        self.hd_layer5 = nn.Linear(64, 32)
        self.hd_layer6 = nn.Linear(32, 64)
        self.hd_layer7 = nn.Linear(64, 32)
        self.hd_layer8 = nn.Linear(32, 16)
        self.hd_layer9 = nn.Linear(16, 8)
        
        # 11. 출력층 8 -> 1
        self.out_layer = nn.Linear(8, 1)

        # LeakyReLU (alpha=0.01 사용)
        self.leaky_relu = nn.LeakyReLU(0.01)

    def forward(self, input_data):
        # 1. 입력층
        y = self.leaky_relu(self.in_layer(input_data))
        
        # 2~10. 은닉층들에 LeakyReLU 적용
        y = self.leaky_relu(self.hd_layer1(y))
        y = self.leaky_relu(self.hd_layer2(y))
        y = self.leaky_relu(self.hd_layer3(y))
        y = self.leaky_relu(self.hd_layer4(y))
        y = self.leaky_relu(self.hd_layer5(y))
        y = self.leaky_relu(self.hd_layer6(y))
        y = self.leaky_relu(self.hd_layer7(y))
        y = self.leaky_relu(self.hd_layer8(y))
        y = self.leaky_relu(self.hd_layer9(y))
        
        # 11. 출력층 (활성화 함수 없음, 회귀이므로)                                     q                                                                                                                               

        
        return self.out_layer(y)

    # 모델 정의
class SoftmaxClassifier(nn.Module):
    def __init__(self, input_dim=4, output_dim=1):  
        super(SoftmaxClassifier, self).__init__()  
        self.fc1 = nn.Linear(input_dim, 512)
        self.bn1 = nn.BatchNorm1d(512)
        self.fc2 = nn.Linear(512, 256)
        self.bn2 = nn.BatchNorm1d(256)
        self.fc3 = nn.Linear(256, 128)
        self.bn3 = nn.BatchNorm1d(128)
        self.fc4 = nn.Linear(128, 64)
        self.bn4 = nn.BatchNorm1d(64)
        self.fc5 = nn.Linear(64, 32)
        self.bn5 = nn.BatchNorm1d(32)
        self.fc6 = nn.Linear(32, 16)
        self.bn6 = nn.BatchNorm1d(16)
        self.fc7 = nn.Linear(16, 8)
        self.bn7 = nn.BatchNorm1d(8)
        self.fc8 = nn.Linear(8, 4)
        self.bn8 = nn.BatchNorm1d(4)
        self.fc9 = nn.Linear(4, 2)
        self.fc10 = nn.Linear(2, output_dim)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.bn1(self.fc1(x)))
        x = self.relu(self.bn2(self.fc2(x)))
        x = self.relu(self.bn3(self.fc3(x)))
        x = self.relu(self.bn4(self.fc4(x)))
        x = self.relu(self.bn5(self.fc5(x)))
        x = self.relu(self.bn6(self.fc6(x)))
        x = self.relu(self.bn7(self.fc7(x)))
        x = self.relu(self.bn8(self.fc8(x)))
        x = self.fc9(x)
        logits = self.fc10(x)
        return logits


