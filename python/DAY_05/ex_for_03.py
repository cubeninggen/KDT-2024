#---------------------------------------------------------------------------------------------
# 제어문 - 반복문
#---------------------------------------------------------------------------------------------
# [실습] 출력하고 싶은 단을 입력 받아서 
#        해당 단의 구구단을 출력하세요.
#---------------------------------------------------------------------------------------------
num=int(input('출력 할 단의 수 : ').strip())
for i in range(1,10):
    print(f'{num} * {i} = {num*i}')