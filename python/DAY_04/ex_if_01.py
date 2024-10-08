#-----------------------------------------------------------------------------------------------
# 제어문 중 조건문 살펴보기
# - 조건에 만족하는 경우 즉, Ture가 되면 실행되는 코드와 실행되지 않는 코드를 결정하는 문법
# - 형식
#   if 조건식:
#   ----실행코드
#   ----실행코드
#   코드
#-----------------------------------------------------------------------------------------------
# => 다중조건문
# - 조건이 2개 이상인 경우
# - 형식
#   if 조건1:
#   ----실행코드
#   elif 조건2:
#   ----실행코드
#   elif 조건3:
#   ----실행코드
#        :
#   elif 조건n:
#   ----실행코드
#   else:
#   ----실행코드
#   코드
#-----------------------------------------------------------------------------------------------
# [실습] 나이에 따른 대구 버스 요금(현금) 출력하기
# - 무료 : 0~5세까지, 65세이상
# - 500원 : 6~12세까지
# - 1000원 : 13~19세까지
# - 1700원 : 20~ 세까지
#-----------------------------------------------------------------------------------------------
age=int(input('현제 나이 입력 : '))
bus=['무료','500원','1000원','1700원']
if age<=5:
    print(f'나이 {age}세는 버스 요금이 {bus[0]}입니다.')
elif age<=12:
    print(f'나이 {age}세는 버스 요금이 {bus[1]}입니다.')
elif age<=19:
    print(f'나이 {age}세는 버스 요금이 {bus[2]}입니다.')
elif age<=64:
    print(f'나이 {age}세는 버스 요금이 {bus[3]}입니다.')
else:
    print(f'나이 {age}세는 버스 요금이 {bus[0]}입니다.')

