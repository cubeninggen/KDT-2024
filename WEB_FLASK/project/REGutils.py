import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt 
import os

# 데이터셋 분리
class SeperateSet():
    def __init__(self,feature,target):
        self.feature=feature
        self.target=target
    
    def run(self):
        ''' output= X_train,X_val,X_test,y_train,y_val,y_test '''
        X_train,X_test,y_train,y_test=train_test_split(self.feature,self.target,test_size=0.2,random_state=1)
        X_train,X_val,y_train,y_val=train_test_split(X_train,y_train,test_size=0.2,random_state=1)
        return X_train,X_val,X_test,y_train,y_val,y_test

    

class DynamicsModel(nn.Module):
    def __init__(self,in_in,out_out,nums=[]):
        super().__init__()
        self.in_layer=nn.Linear(in_in,nums[0] if len(nums) else 5)
        self.h_layer=nn.ModuleList()
        for n in range(len(nums)-1):
            self.h_layer.append(nn.Linear(nums[n],nums[n+1]))
        self.out_layer=nn.Linear(nums[-1] if len(nums) else 5,out_out)

    def forward(self,x):
        x=F.relu(self.in_layer(x))
        for module in self.h_layer:
            x=F.leaky_relu(module(x))
        return self.out_layer(x)
    


class MyDataSet(Dataset):
    def __init__(self,feature,target):
        """ feature 와 target 이 DataFrame 일때"""
        self.feature=feature
        self.target=target
        self.n_rows=feature.shape[0]

    def __len__(self):
        return self.n_rows
    
    def __getitem__(self,index):
        featureTS=torch.FloatTensor(self.feature.iloc[index].values)
        targetTS=torch.FloatTensor(self.target.iloc[index].values)
        return featureTS,targetTS


class Train_val():
    def __init__ (self,trainDL,valDL,model,optimizer,lossF,scoreF):
        self.trainDL=trainDL
        self.valDL=valDL
        self.model=model
        self.lossF=lossF
        self.scoreF=scoreF
        self.optimizer=optimizer
    
    def train(self,EPOCH,scheduler,modelnum):
        HISTORY={'loss':[[],[]],'score':[[],[]]}

        self.model.train()
        for epoch in range(EPOCH):

            loss_total=0
            score_total=0

            for feature,target in self.trainDL:
                pre_y=self.model(feature)
                loss=self.lossF(pre_y,target)
                score=self.scoreF(pre_y,target)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                loss_total+=loss.item()
                score_total+=score.item()

            HISTORY['loss'][0].append(loss_total/len(self.trainDL))
            HISTORY['score'][0].append(score_total/len(self.trainDL))

            self.model.eval()
            with torch.no_grad():
                for feature,target in self.valDL:
                    val_pre_y=self.model(feature)

                    loss=self.lossF(val_pre_y,target)
                    score=self.scoreF(val_pre_y,target)
                
                HISTORY['loss'][1].append(loss.item())
                HISTORY['score'][1].append(score.item())

            # 모델 폴더가 없다면 생성
            if not os.path.exists('model/'):
                os.mkdir('model/')

            # test loss가 최저인점 저장
            if len(HISTORY['loss'][1])==1:
                torch.save(self.model,f'model/best_model{modelnum}.pth')
                # torch.save(self.model.state_dict(),f'model/best_weight{modelnum}.pth')
        
            elif HISTORY['loss'][1][-1]<=min(HISTORY['loss'][1]):
                torch.save(self.model,f'model/best_model{modelnum}.pth')
                # torch.save(self.model.state_dict(),f'model/best_weight{modelnum}.pth')


        
            
            print(f'[{epoch+1}/{EPOCH}]')
            print(f"train loss {HISTORY['loss'][0][-1]}, train score {HISTORY['score'][0][-1]}")
            print(f"test loss {HISTORY['loss'][1][-1]}, test score {HISTORY['score'][1][-1]}")
            
            # test loss 기준으로 스케쥴러 실행
            scheduler.step(HISTORY['loss'][1][-1])
            print(f'scheduler.num_bad_epochs { scheduler.num_bad_epochs}/{ scheduler.patience}')

            if scheduler.num_bad_epochs >= scheduler.patience:
                print(f'[{scheduler.patience}] EPOCH 성능개선이 없어서 조기 종료함')
                break

        return HISTORY

class Plot_History():
    def __init__(self,history):
        self.history=history


    def draw(self,num=0):
        fig,axs=plt.subplots(1,2,figsize=(10,5))
        final=len(self.history['loss'][0])
        axs[0].plot(range(1 if num==0 else final-num+1 ,final+1),self.history['loss'][0][-1*num:],label='train')
        axs[0].plot(range(1 if num==0 else final-num+1 ,final+1),self.history['loss'][1][-1*num:],label='val')
        axs[0].set(xlabel='EPOCH',ylabel='loss')
        axs[0].grid()
        axs[0].legend()

        axs[1].plot(range(1 if num==0 else final-num+1 ,final+1),self.history['score'][0][-1*num:],label='train')
        axs[1].plot(range(1 if num==0 else final-num+1 ,final+1),self.history['score'][1][-1*num:],label='val')
        axs[1].set(xlabel='EPOCH',ylabel='score')
        axs[1].grid()
        axs[1].legend()




class DropDynamicsModel(nn.Module):
    def __init__(self,in_in,out_out,nums=[]):
        super().__init__()
        self.in_layer=nn.Linear(in_in,nums[0] if len(nums) else 5)
        self.h_layer=nn.ModuleList()
        for n in range(len(nums)-1):
            self.h_layer.append(nn.Linear(nums[n],nums[n+1]))
            self.dropout=nn.Dropout(0.5)
        self.out_layer=nn.Linear(nums[-1] if len(nums) else 5,out_out)

    def forward(self,x):
        x=F.relu(self.in_layer(x))
        for module in self.h_layer:
            x=F.relu(module(x))
            x=self.dropout(x)
        return self.out_layer(x)
    

    

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
        
        # 11. 출력층 (활성화 함수 없음, 회귀이므로)
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


