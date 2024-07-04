# 중첩 for 구구단 일반 for로 줄이기
for i in range(10,100):
    print() if i%10==0 else print(f'{i%10}*{i//10}={(i//10)*(i%10):^2}',end='|')
print()
# 구구단 가로로 출력
# 2~5단 줄바꾸고6~9단
for i in range(1,10):
    print()
    for j in range(2,6):
        print(f'{j}*{i}={j*i:^2}',end='|')
print()  
for i in range(1,10):
    print()
    for j in range(6,10):
        print(f'{j}*{i}={j*i:^2}',end='|')
print()

# 17-5
i=2
j=5
while i<=32 or j>=1:
    print(i,j)
    i*=2
    j-=1

# 17-6
num=int(input('잔액 입력 : ').strip())
while num>0:
    num-=1350
    print(num)

# 18-5
i=0
while True:
    if i%10!=3:
        i+=1
        continue
    if i>73:
        break
    print(i,end=' ')
    i+=1
print()

# 18-6
start,stop=map(int,input('입력 : ').split())
i=start
while True:
    if i%10==3:
        i+=1
        continue
    if i>stop:
        break
    print(i,end=' ')
    i+=1
print()

# 19-5
for i in range(5):
    for j in range(5):
        if j<i:
            print(' ',end='')
        else:
            print('*',end='')
    print()
print()

# 19-6
num=int(input('숫자 입력 : ').strip())
for i in range(num):
    for j in reversed(range(num)):
        if i<j:
            print(' ',end='')
        else:
            print('*',end='')
    for j in range(num):
        if i>j:
            print('*',end='')
    print()
print()

num=int(input().strip())
for i in range(1,num+1):
    print(' '*(num-1)+'*'*(2*i-1))

# 20-7
for i in range(1,101):
    if i%2==0 and i%11==0:
        print('FizzBuzz')
    elif i%2==0:
        print('Fizz')
    elif i%11==0:
        print('Buzz')
    else:
        print(i)
print()

# 20-8
a,b=map(int,input().split())
for i in range(a,b+1):
    if i%5==0 and i%7==0:
        print('FizzBuzz')
    elif i%5==0:
        print('Fizz')
    elif i%7==0:
        print('Buzz')
    else:
        print(i)
