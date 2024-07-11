#----------------------------------------------------------------------------------------
# Dict 전용 함수 즉, 메서드
# -> keys(),values(),items()
#----------------------------------------------------------------------------------------
person={'name':'홍길동','age':10}
#[메서드 - 값 읽어오는 메서드 get(key)]
# - key에 해당하는 value가 없으면 default값을 반환
print(person['name'])

print(person.get('name','몰라'))
print(person.get('gender','없음'))
print(person.get('gender'))

#[메서드 - 키와 값 추가 메서드 get(key)]
person['gender']='남'

#[메서드 - 수정 및 업데이트 메서드 update(key=value)]
person['gender']='여'

person.update(gender='어린이')
print(person)

person.update(gender='어린이',job='학생')
print(person)

person.update({'phone':'010','birth':'202401041'})#덩어리로
print(person)

person.update(**{'weight':100,'height':170})# 풀어서 요소별로 K:V
print(person)


msg='Hello Good Luck'
alpha=set(msg)
save={}
for i in alpha:
    print(i,msg.count(i))
    save[i]=msg.count(i)
print(save)

