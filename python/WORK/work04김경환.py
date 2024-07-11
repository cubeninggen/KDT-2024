# 12-4
camille={
    'health':575.6,
    'health_regen':1.7,
    'mana':338.3,
    'mana_regen':1.63,
    'melee':125,
    'attack_damage':60,
    'attack_speed':0.625,
    'amor':26,
    'magic_resistance':32.1,
    'movement_speed':340
}
print(camille['health'])
print(camille['movement_speed'])

# 12-5
player_key=input('key : ').split()
player_value=list(map(float,input('value : ').split()))

print(dict(zip(player_key,player_value)))

# 13-6
x=5
if x!=10:
    print('ok')

# 13-7
price=input('가격 입력 : ').strip()
discount=input('쿠폰 입력 : ').strip()
if discount=='Chash3000':
    print(int(price)-3000)
else:
    print(int(price)-5000)

# 14-6
written_test=75
cording_test=True
if written_test>=80 and cording_test==True:
    print('합격')
else:
    print('불합격')

# 14-7
grade=list(map(int,input('점수 입력 : ').split()))
if 100>=grade[0]>=0 and 100>=grade[1]>=0 and 100>=grade[2]>=0 and 100>=grade[3]>=0:
    if sum(grade)/len(grade)>=80:
        print('합격')
    else:
        print('불합격')
else:
    ('잘못된 정수 입니다.')

# 15-3
x=int(input())
if 11<=x<=20:
    print('11~20')
elif 21<=x<=30:
    print('21~30')
else:
    ('아무것도 해당하지 않음')

# 15-4
age=int(input())
balance=9000
if 7<=age<=12:
    balance=balance-650
elif 13<=age<=18:
    balance=balance-1050
else:
    balance=balance-1250 
print(balance)


