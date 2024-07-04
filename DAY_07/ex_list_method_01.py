#---------------------------------------------------------------------------------------------
# 리스트 전용의 함수 즉, 메서드(method)
# - 리스트의 원소/요소를 제어하기 위한 홤수들
#---------------------------------------------------------------------------------------------
import random as rad

# [1] 실습 데이터 => 임의의 정수 숫자10개 구성된 리스트
datas=[1,2,3,3,3,4,5,6,7,8,9,10]

# [메서드 - 요소 인덱스를 반환하는 메서드 index()]
# -> 11의 인덱스를 찾기
# -> 왼쪽 >>> 오른쪽으로 찾기
idx=datas.index(6)
print(f'6의 인덱스 : {idx}')

# -> 0의 인덱스를 찾기 ==> 존제하지 않는 데이터의 경우 ERROR
num=int(input())
if num in datas:
    idx=datas.index(num)
    print(f'{num}의 첫번째 인덱스 : {idx}')
    num in datas
    idx=datas.index(num,idx+1)
    print(f'{num}의 두번째 인덱스 : {idx}')
    num in datas
    idx=datas.index(num,idx+1)
    print(f'{num}의 세번째 인덱스 : {idx}')
else:
    print(f'{num}은 존제하지 않는 데이터 입니다.')


# [메서드 - 데이터가 몇개 존제하는지 갯수 파악하는 메서드 count()]
cnt=datas.count(num)
print(f'{num}의 갯수 : {cnt}개')
idx=0
if num in datas:
    for i in range(cnt):
        idx=datas.index(num,idx if not i else idx+1)
        print(f'{i+1}번쨰 {num}의 인덱스 : {idx}')
else:
    print(f'{num}은 존제하지 않는 데이터 입니다.')