#---------------------------------------------------------------------------------------------
# 제어문 - 반복문
#---------------------------------------------------------------------------------------------
# [실습] 2단 ~ 9단까지 모두 출력하세요.
#---------------------------------------------------------------------------------------------
for j in range(1,10):
    print()
    for i in range(2,10):
        print(f'{i} * {j} = {j*i}',end='|')