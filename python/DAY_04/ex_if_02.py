#-----------------------------------------------------------------------------------------------
# [실습] 숫자를 입력 받아서 음이 아닌 정수와 음수 수분하기
#-----------------------------------------------------------------------------------------------
num=int(input('비교할 숫자 : ').strip())
if num>=0:
    print(f'숫자 {num}은 음이 아닌 정수 입니다')
else:
    print(f'숫자 {num}은 음수 입니다')
#-----------------------------------------------------------------------------------------------
# [실습] 점수를 입력 받아서 합격과 불합격 출력
## - 합격 60점 이상 
#-----------------------------------------------------------------------------------------------
num=int(input('점수 : ').strip())
if num>=60:
    print('합격')
else:
    print('불합격')
#-----------------------------------------------------------------------------------------------
# [실습] 점수를 입력 받아서 학점 출력
## - 학점 : A90, B80, C70, D60, F50 
#-----------------------------------------------------------------------------------------------
num=int(input('점수 : ').strip())
if num>=90:
    print('당신의 학점은 : A')
elif num>=80:
    print('당신의 학점은 : B')
elif num>=70:
    print('당신의 학점은 : C')
elif num>=60:
    print('당신의 학점은 : D')
else:
    print('당신의 학점은 : F')