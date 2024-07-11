#------------------------------------------------------------------------------------------
# 함수와 면수 - 지역/전역 변수
#------------------------------------------------------------------------------------------
## 전역변수
persons=['Hong']
gender={'h':'남자'}
year=2024
## 사용자 정의 함수
def add_person(name):
    global year 
    year+=1
    persons.append(name)
    gender[name]='여'

def remove_person(name):
    persons.remove(name)
    gender.pop(name)

## 실행 즉, 함수 호출
print(f'resons => {persons}')
add_person('Park')
print(f'resons => {persons}')
print(f'gender => {gender}')
remove_person('Park')
print(f'resons => {persons}')
print(f'gender => {gender}')