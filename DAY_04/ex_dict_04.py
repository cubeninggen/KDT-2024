#-----------------------------------------------------------------------------------------------
# Dict 자료형 살펴보기
# - 연산자와 내장함수
#-----------------------------------------------------------------------------------------------
person={'name':'홍길동','age':20,'job':'학생'}
dog={'type':'afgan hound','weight':'3kg','color':'black','gender':'male','age':5}
grade={'국어':90,'수학':178,'채육':100}
##[연산자]
# 산술 연산X 
# person+dog

# 맴버연산자 : in, not in
print('name'in dog)
print('name'in person)

# dict 에서는 key로만 멤버연산가능
# print('afgan hound'in dog)
# print(20 in person) 

# value 추출
print('afgan hound'in dog.values())
print(20 in person.values())

## [내장함수]
## - 원소/요소 개수 확인 : len()
print(f'dog의 요소 개수 : {len(dog)}개')
print(f'person의 요소 개수 : {len(person)}개')

## - 원소/요소 정렬 : sorted()
#  - 키만 정렬
print(f'dog 오름차순정렬 : {sorted(dog)}')
print(f'dog 내림차순정렬 : {sorted(dog,reverse=True)}')

print(f'grade 값 오름차순정렬 : {sorted(grade.values())}')
print(f'grade 키 오름차순정렬 : {sorted(grade)}')
# grade 값 오름차순정렬 : [90, 100, 178]
# grade 키 오름차순정렬 : ['국어', '수학', '채육']

print(f'grade 값 오름차순정렬 : {sorted(grade.items())}')
# grade 값 오름차순정렬 : [('국어', 90), ('수학', 178), ('채육', 100)]
print(f'grade 값 오름차순정렬 : {sorted(grade.items(),key=lambda x:x[1])}')# tuple 타입 반환값에서 1번자리 인덱스로 접근

# print(f'dog 오름차순정렬 : {sorted(dog.values)}') <== 복합 type 이라 안됨
