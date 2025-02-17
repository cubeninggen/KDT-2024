#--------------------------------------------------------------------------------------------
# str 데이터 타입 전용 함수 즉, 메서드 살펴보기
#--------------------------------------------------------------------------------------------
## [문자열에서 좌우 여백 제거 메서드 -> strip(), lstrip(), rstrip()]
## - 주의 : 문자열 내부에 공백 제거는 X
msg='Good Luck'
data=' Happy New Year 2025!  '

# 좌우 모든 공백 제거
m1=msg.strip()
print(f'뭔본 msg : {len(msg)}개 --- 제거 m1 : {len(m1)}개')

d1=data.strip()
print(f'뭔본 data : {len(data)}개 --- 제거 d1 : {len(d1)}개')

# 왼쪽 즉, 문자열 시작 부분의 공백 제거
d1=data.lstrip()
print(f'뭔본 data : {len(data)}개 --- 제거 d1 : {len(d1)}개')

# 오른쪽 즉, 문자열 끝 부분의 공백 제거
d1=data.rstrip()
print(f'뭔본 data : {len(data)}개 --- 제거 d1 : {len(d1)}개')

## [실습] 이름을 입력 받아서 저장하세요
## - input()함수 사용
name=input('이름 : ').strip()
if len(name)>0:
    print(f'name : {name}, {len(name)}')
else:
    print('이름을 입력해 주십시요.')

## [실습] 입력 받은 데이터에 따라 출력을 다르게 합니다
## - input()함수 사용
data=input('알파벳 또는 문자 1개 입력 : ').strip()
if not 0<data<1:
    print('한개의 문자만 입력해주세요.')
else:
    if 'a'<=data<='z' or 'A'<=data<='Z':
        print('★')
    elif '0'<=data<='9':
        print('♥')
    else:
        print('알파벳 또는 문자만 입력해 주세요.')