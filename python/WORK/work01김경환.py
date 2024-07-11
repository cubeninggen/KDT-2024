# 3-7
print('Hello, World!')
print('Python Programming')

# 3-8
print('Hello, World!')
print('Hello, World!')

# 5-5
print('아파트에서 소음이 가장 심한 층수')
print('도로와의 거리 : 12m')
print(int(0.2467 * 12 +4.159))

# 5-6 
print('L 게임의 왜곡 스킬 산정식 : AP * 0.6 + 255')
print('AP = 102')
print(102*0.6+225)

# 6-3.4
a=int(input('첫 번째 숫자를 입력하세요: '))
b=int(input('두 번째 숫자를 입력하세요: '))
print(a+b)

# 6-4
a,b=input('문자열 두 개를 입력하세요: ').split()
print(a)
print(b)

# 6-4.1
a,b=input('숫자 두 개를 입력하세요: ').split()
print(a+b)

# 6-4.2
a,b=input('숫자 두 개를 입력하세요: ').split()
a=int(a)
b=int(b)
print(a+b)

# 6-4.3
a,b=map(int, input('숫자 두 개를 입력하세요: ').split())
print(a+b)

# 6-4.4
a,b=map(int, input('숫자 두 개를 입력하세요: ').split(','))
print(a+b)

# 6-6
a,b,c=map(int,input().split())
print(a+b+c)

# 6-7
a,b,c=input().split()
print(a)
print(b)
print(c)

# 6-8
a,b,c,d=map(int,input().split())
print((a+b+c+d)/4)

# 7-2.1
print(1)
print(2)
print(3)

print(1,end='')
print(2,end='')
print(3)

print(1,end=' ')
print(2,end=' ')
print(3)

# 7-4
year=2000
month=10
day=27
hour=11
minute=43
second=59

print(year,month,day,sep='/',end='\n')
print(day,hour,second,sep=':')

# 7-5
year,month,day,hour,minute,second=input().split()

print(year,month,day,sep='/',end='T')
print(day,hour,second,sep=':')

# 8-4 
korean=92
english=47
mathematics=86
science=81

print(korean>=50 and english>=50 and mathematics>=50 and science>=50)

# 8-4
korean,english,mathematics,science=map(int,input().split())
print(korean>=90 and english>80 and mathematics>85 and science>=80)

# 9-3
s=''' python is a programming language that lets you work quickly
and
integrate systems more effectively'''
print(s)

# 9-4
s=''' 'python' is a "programming language" 
that lets you work quickly
and
integrate systems more effectively'''
print(s)