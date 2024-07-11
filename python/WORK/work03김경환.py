#001
print('Hello World')

#002
print("Mary's cosmetics")

#003
print('신씨가 소리질렀다. "도둑이야".')

#004
print("C:\\Windows")

#005
print("안녕하세요.\n만나서\t\t반갑습니다.")
# \n은 줄바꿈 \t는 탭을 의미합니다.

#006
print ("오늘은", "일요일")
# 오늘은 일요일

#007
print('naver','kakao','sk','samsung',sep=';')

#008
print('naver','kakao','sk','samsung',sep='/')

#009
print("first",end='')
print("second")

#010
print(f'5 / 3 = {5/3}')

#011
삼성전자=50000
총평가금액=삼성전자*10
print(총평가금액)

#012
시가총액=298000000000000
현재가=50000
per=15.79
print(시가총액,type(시가총액))
print(현재가,type(현재가))
print(per,type(per))

#013
s="hello"
t="python"
print(s+'!',t)

#014
a=2+2*3
# 8

#015
a='132'
print(type(a))

#016
num='720'
print(int(num))

#017
num=100
print(str(num))

#018
msg='15.79'
print(float(msg))

#019
year='2020'
year=int(year)
print(year-3,year-2,year-1)

#020
month_fee=48584
total_month=36
print(month_fee*total_month)

#021
letters = 'python'
print(letters[0],letters[2])

#022
license_plate = "24가 2210"
print(license_plate[-4:])

#023
string = "홀짝홀짝홀짝"
print(string[::2])

#024
string = "PYTHON"
print(string[::-1])

#025
phone_number = "010-1111-2222"
phone_number=phone_number.replace('-',' ')
print(phone_number)

#026
phone_number = "010-1111-2222"
phone_number=phone_number.replace('-','')
print(phone_number)

#027
url = "http://sharebook.kr"
url=url.split('.')
print(url[-1])

#028
# lang = 'python'
# lang[0] = 'P'
# print(lang)
# 문자열은 수정이 불가하므로 애러출력
# TypeError: 'str' object does not support item assignment

#029
string = 'abcdfe2a354a32a'
string=string.replace('a','A')
print(string)

#030
string = 'abcd'
string.replace('b', 'B')
print(string)
# 리플레이스 시킨 문자열에 대하여 변수할당이 되지않았고
# string변수는 여전히 'abcd'를 가리키므로 'abcd'가 출력됩니다

#031
a = "3"
b = "4"
print(a + b)
# "34"

#032
print("Hi" * 3)
# HiHiHi

#033
print('-'*80)

#034
t1 = 'python'
t2 = 'java'
print((t1+' '+t2+' ')*4)

#035
name1 = "김민수" 
age1 = 10
name2 = "이철희"
age2 = 13
print('이름: %s 나이: %d'%(name1,age1))
print('이름: %s 나이: %d'%(name2,age2))

#036
print('이름: {} 나이: {}'.format(name1,age1))
print('이름: {} 나이: {}'.format(name2,age2))

#037
print(f'이름: {name1} 나이: {age1}')
print(f'이름: {name2} 나이: {age2}')

#038
상장주식수 = "5,969,782,550"
print(int(상장주식수.replace(',','')),type(int(상장주식수.replace(',',''))))

#039
분기 = "2020/03(E) (IFRS연결)"
print(분기[:7])

#040
data = "   삼성전자    "
print(data.strip())

#041
ticker = "btc_krw"
print(ticker.upper())

#042
ticker = "BTC_KRW"
print(ticker.lower())

#043
msg='hello'
print(msg.capitalize())

#044
file_name = "보고서.xlsx"
print(file_name.endswith('xlsx'))

#045
file_name = "보고서.xlsx"
print(file_name.endswith(('xlsx','xls')))

#046
file_name = "2020_보고서.xlsx"
print(file_name.startswith('2020'))

#047
a = "hello world"
print(a.split())

#048
ticker = "btc_krw"
print(ticker.split('_'))

#049
date = "2020-05-01"
print(date.split('-'))

#050
data = "039490     "
print(data.strip())

#051
movie_rank=['닥터 스트레인지','스플릿','럭키']
print(movie_rank)

#052
movie_rank.append('배트맨')
print(movie_rank)

#053
movie_rank.insert(1,'슈퍼맨')
print(movie_rank)

#054
del movie_rank[3]
print(movie_rank)

#055
del movie_rank[2:]
print(movie_rank)

#056
lang1=["C", "C++", "JAVA"]
lang2=["Python", "Go", "C#"]
lang3=lang1+lang2
print(lang3)

#057
nums = [1, 2, 3, 4, 5, 6, 7]
print(f'max: {max(nums)}')
print(f'min: {min(nums)}')

#058
nums = [1, 2, 3, 4, 5]
print(sum(nums))

#059
cook = ["피자", "김밥", "만두", "양념치킨", "족발", "피자", "김치만두", "쫄면", "소시지", "라면", "팥빙수", "김치전"]
print(len(cook))

#060
nums = [1, 2, 3, 4, 5]
print(sum(nums)/len(nums))

#061
price = ['20180728', 100, 130, 140, 150, 160, 170]
print(price[1:])

#062
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(nums[::2])

#063
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(nums[1::2])

#064
nums = [1, 2, 3, 4, 5]
print(nums[::-1])

#065
interest = ['삼성전자', 'LG전자', 'Naver']
print(interest[0],interest[2])

#066
interest = ['삼성전자', 'LG전자', 'Naver', 'SK하이닉스', '미래에셋대우']
print(' '.join(interest))

#067
interest = ['삼성전자', 'LG전자', 'Naver', 'SK하이닉스', '미래에셋대우']
print('/'.join(interest))

#068
interest = ['삼성전자', 'LG전자', 'Naver', 'SK하이닉스', '미래에셋대우']
print('\n'.join(interest))

#069
string = "삼성전자/LG전자/Naver"
print(string.split('/'))

#070
data = [2, 4, 3, 1, 5, 10, 9]
data.sort()
print(data)

#071
my_variable=()

#072
movie_rank=('닥터 스트레인지','스플릿','럭키')

#073
num=(1,)

#074
# >> t = (1, 2, 3)
# >> t[0] = 'a'
# Traceback (most recent call last):
#   File "<pyshell#46>", line 1, in <module>
#     t[0] = 'a'
# TypeError: 'tuple' object does not support item assignment
# 튜플은 원소수정이 안됨

#075
t = 1, 2, 3, 4
print(type(t))
# 튜플은 괄호 생략도 가능함

#076
t = ('a', 'b', 'c')
t = ('A', 'b', 'c')
print(t)

#077
interest = ('삼성전자', 'LG전자', 'SK Hynix')
interest=list(interest)
print(type(interest))

#078
interest = ['삼성전자', 'LG전자', 'SK Hynix']
interest=tuple(interest)

#079
temp = ('apple', 'banana', 'cake')
a, b, c = temp
print(a, b, c)
# apple banana cake

#080
data=tuple(range(2,100,2))
print(data)
