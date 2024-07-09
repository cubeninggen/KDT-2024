def cal(num1,sim,num2):
    if sim=='+':return num1+num2
    elif sim=='-':return num1-num2
    elif sim=='*':return num1*num2
    elif sim=='/':
        if not num2==0:
            return num1/num2
        else:
            result2=num1
            return '0으로 나눌 수 없습니다.'
    else:return '올바른 계산식을 입력해주세요'
def history(msg1,msg2,msg3,msg4):
    if type(msg4)==type('0'):
        data.append('ERROR')
    else:
        data.append(str(msg1)+str(msg2)+str(msg3)+'='+str(msg4))
    print('history :',end=' ')
    for i in data:
        print(i,end=' ')
    print()
def err_his():
    data.append('ERROR')
    print('history :',end=' ')
    for i in data:
        print(i,end=' ')
    print()
data=[]
result=0
result1=0
result2=0
while True:
    print('초기화 c or C | 종료 x or X')
    req=input('계산할 식을 띄어쓰기로 구분해서 입력하세요(1 + 2 |or| + 2) : ').strip().split()
    if len(req)==0:
        print('계산식을 입력해주세요')
    elif req[0]=='x' or req[0]=='X':
        ny=input('종료 하시겠습니까?(y/n) :')
        if ny=='y':
            print('계산기를 종료합니다')
            break
        else:print('종료 취소')
    elif req[0]=='c' or req[0]=='C':
        nory=input('초기화 하시겠습니까?(y/n) :')
        if nory=='y':
            data=[]
            result=0
            result1=0
            print('초기화가 완료되었습니다.')
            print('history :')
            print(f'이전 결과값 : {result}')
        else:print('초기화 취소')
    elif len(req)==3 and req[0].strip('-').isdigit() and req[2].strip('-').isdigit():
        if result:
            yorn=input('이미 연산된 결과가 존제합니다.\n연산결과를 덮어 씌우겠습니까?(y/n) : ')
            if yorn=='y':
                result=cal(int(req[0]),req[1],int(req[2]))
                print(f'{req[0]}{req[1]}{req[2]}={result}')
                req[0]='(pasted)'+str(req[0])
                history(req[0],req[1],req[2],result)
                if type(result)==type('0'):
                    result=result2
            elif yorn=='n':
                redo=input('덮어쓰기를 취소했습니다.\n현제 연산결과를 기존결과값과 연산하시려면 원하는 연산부호를 입력해주세요. : ')
                if redo=='+' or redo=='-' or redo=='*' or redo=='/':
                    result1=cal(result,redo,cal(int(req[0]),req[1],int(req[2])))
                    print(f'{result}{redo}{cal(int(req[0]),req[1],int(req[2]))}={result1}')
                    history(result,redo,cal(int(req[0]),req[1],int(req[2])),result1)
                    if type(result1)==type('0'):
                        result1=result2
                else:
                    print('잘못된 입력입니다 다시 입력하세요.')
                    err_his()  
            else:
                print('잘못된 입력입니다 다시 입력하세요.')
                err_his()
        else:
            result=cal(int(req[0]),req[1],int(req[2]))
            print(f'{req[0]}{req[1]}{req[2]}={result}')
            history(req[0],req[1],req[2],result)
            if type(result)==type('0'):
                result=result2
    elif len(req)==2 and req[1].strip('-').isdigit():
        result1=cal(result,req[0],int(req[1]))
        print(f'{result}{req[0]}{req[1]}={result1}')
        history(result,req[0],req[1],result1)
        if type(result1)==type('0'):
            result2=result
        else:result=result1
    elif len(req)>3:
        print('이 프로그렘은 2개의 인자만 받습니다.')
        err_his()
    else:
        print('계산식을 입력해주세요')
        err_his()