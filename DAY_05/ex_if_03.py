#------------------------------------------------------------------------------------------
# ==> 조건부표현식 : 조건이 2개 이상인 경우
#------------------------------------------------------------------------------------------
## [실습] 숫자가 양수, 영, 음수 인지 판별
num=int(input('비교할 숫자 입력 : ').strip())
result='양수' if num>0 else '음수' if num<0 else '영'
print(f'{num}은 {result}')