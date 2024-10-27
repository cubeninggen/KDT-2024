#----------------------------------------------------------------------------
# Flask Framework에서 모듈단위 URL 처리 파일
# - 파일명 : main_view.py
# -----------------------------------------------------------------------------
# 모듈로딩
from flask import Blueprint,render_template,url_for,request
#from PROWEB.models.models import Result
from werkzeug.utils import redirect
import torch
import torch.nn as nn
from __init__ import IrisRegModel
from PROWEB.models.models import SoftmaxClassifier
import REGutils
import models



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



# Blueprint 인스턴스 생성
mainBP=Blueprint('main',
                 import_name=__name__,
                 url_prefix='/',
                 template_folder='templates')

model1=torch.load('PROWEB/models/best_model1.pth',weights_only=False)
model2=torch.load('PROWEB/models/best_model2.pth',weights_only=False)
#model3=torch.load('PROWEB/models/best_model3.pth',weights_only=False)

# http://localhost:5000/ URL처리 라우팅 함수 정의
@mainBP.route('/',methods=('GET','POST'))
def index():
    result=0
    if request.method=='POST':
        hum=float(request.form['hum'])
        rain =float(request.form['rain'])
        tem =float(request.form['tem'])
        wind=float(request.form['wind'])

        result1=model1(torch.FloatTensor([hum,rain,tem,wind])).item()
        #result2=model2(torch.FloatTensor([hum,rain,tem,wind])).item()
        #result3=model3(torch.FloatTensor([[hum,rain,tem,wind]])).item()
        #result2=predict2([hum,rain,tem,wind]    )
        result2=55 
        result3=12
        h=result1/(result1+result2+result3)
        g=result2/(result1+result2+result3)
        f=result3/(result1+result2+result3)

        return redirect(url_for('main.Result',result1=h,result2=g,result3=f))
    return render_template('index.html')
    #return redirect(url_for('main.Result',result=0))




@mainBP.route('/result',methods=('POST','GET'))
def Result():

    result1 = request.args.get('result1', 0)
    result2 = request.args.get('result2', 0)
    result3 = request.args.get('result3', 0) 

    return render_template('index copy.html',result1=result1,result2=result2,result3=result3)
    #return redirect(url_for('main.Result',result=result))

