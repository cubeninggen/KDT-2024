#--------------------------------------------------------------------------------------------
# 내가 만든 함수들
#--------------------------------------------------------------------------------------------
def plu(num1,num2):return num1+num2
def min(num1,num2):return num1-num2
def sqe(num1,num2):return num1*num2
def div(num1,num2):return num1/num2 if num2 else '0으로 나눌수 없음'

print(f'__name__ : {__name__}')
if __name__=='__main__':
    print('--test--')
    print(f'결과:{plu(100,100)}')