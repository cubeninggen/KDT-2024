# 16-5
x=[49,-17,25,102,8,62,21]
for i in x:
    print(i*10,end=' ')

print()
# 16-6
num=int(input('출력 할 단의 수 : ').strip())
for i in range(1,10):
    print(f'{num} * {i} = {num*i}')

# 중첩 for문 구구단 줄이기
for i in range(10,100):
    if i%10==0:
        print()
    else:
        print(f'{i%10}*{i//10}={(i//10)*(i%10)}',end='|')