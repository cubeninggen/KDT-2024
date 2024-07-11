#---------------------------------------------------------------------------------------------
# 리스트 전용의 함수 즉, 메서드(method)
# - 리스트의 원소/요소를 제어하기 위한 홤수들
#---------------------------------------------------------------------------------------------
# [메서드 - 요소 추가 메서드 append(데이터)]
datas=[1,3,5]

# 세로운 데이터 100 추가 : 마지막 요소에 이어서 저장
datas.append(100)
print(f'datas 개수 : {len(datas)}, {datas}')
datas.append(100)
print(f'datas 개수 : {len(datas)}, {datas}')

# [메서드 - 요소 추가 메서드 insert(인덱스,데이터)]
datas.insert(0,300)
print(f'datas 개수 : {len(datas)}, {datas}')
datas.insert(-1,300)
print(f'datas 개수 : {len(datas)}, {datas}')

# [실습 : 임의의 정수 숫자 10개 저장하는 리스트 생성]
import random as rad
data=[]
for i in range(10):
    data.append(int(rad.random()*10000))
print(f'data 개수 : {len(data)}, {data}')

# [메서드 - 요소 삭제 메서드 remove(데이터)]
# - 존제하지 않는 데이터 삭제 시 ERROR 발생!!
datas.remove(300)
print(f'datas 개수 : {len(datas)}, {datas}')
