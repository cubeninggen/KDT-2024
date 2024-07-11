#-------------------------------------------------------------------------------------------
# [실습1] 글자를 입력 받습니다. 입력받은 글자를(a~z, A~Z) 코드값을 출력 합니다.
#-------------------------------------------------------------------------------------------
msg=input('a~z, A~Z의 범위 에서 변환할 1개의 문자 : ').strip()
if len(msg)==1 and 'a'<=msg<='z'or'A'<=msg<='Z':
    print(f'{msg}의 코드값 : {ord(msg)}')
else:
    print('제시된 조건과 다릅니다 입력값을 확인하세요.')
#-------------------------------------------------------------------------------------------
# [실습2] 점수를 입력 받은 후 학점을 출력합니다.
# - 학점 : A+, A, A-, B+, B, B-, C+, C, C-, D+, D, D-, F 
#  A+ : 96~100
#  A  : 95
#  A- : 90~94
#-------------------------------------------------------------------------------------------
grade=int(input('점수를 입력하세요 : ').strip())
sub_grade=''
if 100>=grade>95:sub_grade='A+'
elif grade==95:sub_grade='A'
elif grade>=90:sub_grade='A-'
elif grade>85:sub_grade='B+'
elif grade==85:sub_grade='B'
elif grade>=80:sub_grade='B-'
elif grade>75:sub_grade='C+'
elif grade==75:sub_grade='C'
elif grade>=70:sub_grade='C-'
elif grade>65:sub_grade='D+'
elif grade==65:sub_grade='D'
elif grade>=60:sub_grade='D-'
elif grade>=0:sub_grade='F'
else:print('올바른 점수를 입력하세요')
print(f'{grade}점인 당신은 {sub_grade}입니다')