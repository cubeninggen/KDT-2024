# 22-9
a=['alpha','bravo','charlie','delta','echo','foxtrot','golf','hotel','india']
b=[i for i in a if len(i)==5]

# 22-10
#num1=1~20
#num2=10~30
a,b=input().split()
datas=[]
for i in range(int(a),int(b)+1):
    datas.append(2**i)
del datas[1]
del datas[-2]
print(datas)

# 25-7
maria={'korean':94,'english':91,'mathematics':89,'science':83,}
average=sum(maria.values())/len(maria)
print(average)

# 25-8
keys=input().split()
valuse=map(int,input().split())
x=dict(zip(keys,valuse))
#???
print(x)