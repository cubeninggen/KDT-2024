#-----------------------------------------------------------------------------------------------
# Dict 자료형 살펴보기
# - 데이터의 의미를 함꺠 저장하는 자료형
# - 형태 : {key1:value, key2:value...keyn:value}
# - key는 중복 X, value는 중복 O
# - 데이터 분석 시 파일 데이터 갸져 올 때 많이 사용
#-----------------------------------------------------------------------------------------------
## [Dict 생성]
data={}
print(f'data => {len(data)}개, {type(data)}, {data}')

# 사람에 대한 정보 : 이름, 나이, 성별
data={'name':'마징가','age':100,'gender':'남'}
print(f'data => {len(data)}개, {type(data)}, {data}')

# 강아지에 대한 정보 : 품종, 무게, 색상, 성별, 나이
data={'type':'afgan hound','weight':'3kg','color':'black','gender':'male','age':5}
print(f'data => {len(data)}개, {type(data)}, {data}')

## [Dict 원소/요소 읽기]
data={'type':'afgan hound','weight':'3kg','color':'black','gender':'male','age':5}

# 색상출력
print(f'색상 : {data["color"]}')

# 성별, 품종 출력
print(f'성별 : {data["gender"]}')
print(f'품종 : {data["type"]}')

## [Dict 원소/요소 변경]
# 나이 5살 ==> 6살
data['age']=6
print(data)

# 몸무게 3kg ===> 8kg
data['weight']='8kg'
print(data)

## [Dict 원소/요소 삭제]
# del 변수명[키] or del(변수명[키])
# 성별 데이터 삭제
del data['gender']
print(data)

## [Dict 원소/요소 추가]
# 변수명[세로운 키]=값
# 이름 추가 
data['name']='초코'
print(data)