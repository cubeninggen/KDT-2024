# 24,29,30 번
# 24-4
path='c:\\User\\dojang\\AppData\\Local\\Programs\\Pyton\\Python36-32\\python.exe'
filename=path.split('\\')[-1]
print(filename)

# 24-5
'''the grown-ups' response, this time, was to advise me to lay aside my drawings of boa constrictor, 
whether from the inside or the outside, and devote myself insted to geography, history, arithmetic, 
and grammar. That is why, at the, age of six, I gave up what might have been a magnificent career as 
a painter. I had been disheartened by the failure of my Drawing Number One add my Drawing Number Two. 
Grown-ups never understand anything by themselves, and it is tiresome for children to be always and 
forever explaining things to the.'''
msg=input().split()
count=0
for i in msg:
    if 'the.'>=i>='the':
        count=count+1
    else:continue
print(count)

# 24-6
price=list(map(int,input().split(';')))
price.sort(reverse=True)
cnt=0
for i in price:
    print(f'{i:>9,}')

# 29-7
x=10
y=3
def get_quotient_remainder(a,b):
    return a//b,a%b
quotient,remainder=get_quotient_remainder(x,y)
print('몫: {0}, 나머지: {1}'.format(quotient,remainder))

# 29-8
x,y=map(int,input().split())
def calc(x,y):
    return x+y,x-y,x*y,x/y if not y==0 else '0으로 나눌 수 없습니다.'
a,s,m,d=calc(x,y)
print('덧샘: {0},뺼샘: {1},곱셈: {2},나눗셈: {3}'.format(a,s,m,d))

# 30-6
korean,english,mathematics,science=100,86,81,91
def get_max_score(*ave):
    return max(ave)
max_score=get_max_score(korean,english,mathematics,science)
print('높은 점수:',max_score)
max_score=get_max_score(english,science)
print('높은 점수:',max_score)

# 30-7
korean,english,mathematics,science=map(int,input().split())
def get_min_max_score(*grade):
    return min(grade),max(grade)
def get_average(**ave):
    return sum(ave.values())/len(ave)
min_score,max_score=get_min_max_score(korean,english,mathematics,science)
average_score=get_average(korean=korean,english=english,mathematics=mathematics,science=science)
print('낮은 점수: {0:.2f},높은 점수: {1:.2f},평균 점수: {2:.2f}'.format(min_score,max_score,average_score))
min_score,max_score=get_min_max_score(english,science)
average_score=get_average(english=english,science=science)
print('낮은 점수: {0:.2f},높은 점수: {1:.2f},평균 점수: {2:.2f}'.format(min_score,max_score,average_score))