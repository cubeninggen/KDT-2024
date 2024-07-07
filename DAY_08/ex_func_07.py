#-----------------------------------------------------------------------------------------------------------
# 사용자 정의 함수
#-----------------------------------------------------------------------------------------------------------
# 덧셈, 뺼셈, 곱샘, 나눗셈 함수를 각각만들기
# - 매개변수 : 번수2개, num1, num2
# - 함수결과 : 연산 결과 반환
#-----------------------------------------------------------------------------------------------------------
def plu(num1,num2):return num1+num2
def min(num1,num2):return num1-num2
def sqe(num1,num2):return num1*num2
def div(num1,num2):return num1/num2 if num2 else '0으로 나눌수 없음'

# 함수 사용하기 즉, 호출
# [실습] 사용자로부터 숫자1,연산자,숫자2를 입력 받아서 연산 결과를 출력해주세요.
# - input('숫자1 연산자 숫자2').split()
data=input('연산할 계산식 입력(1 + 2) : ').split()
if len(data)==3 and data[1]in['+','-','*','/']:
    if data[1]=='+':
        print(f'{data[0]}{data[1]}{data[2]}={plu(int(data[0]),int(data[2]))}')
    elif data[1]=='-':
        print(f'{data[0]}{data[1]}{data[2]}={min(int(data[0]),int(data[2]))}')
    elif data[1]=='*':
        print(f'{data[0]}{data[1]}{data[2]}={sqe(int(data[0]),int(data[2]))}')
    elif data[1]=='/':
        print(f'{data[0]}{data[1]}{data[2]}={div(int(data[0]),int(data[2]))}')
else:
    print('올바른 계산식을 입력해주세요.')
