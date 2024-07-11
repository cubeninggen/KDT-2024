# 10-4
a= list(range(5,-10,-2))
print(a)

# 10-5
a=int(input())
b=tuple(range(-10,9,a))
print(b)

# 11-6
year=[2011,2012,2013,2014,2015,2016,2017,2018]
population=[10249679,10195318,10103233,10022181,9930616,9857426,9838892]
print(year[-3:],'\n',population[-3:])

# 11-7
n=-32,75,97,-10,9,32,4,-15,0,76,14,2
print(n[::2])

# 11-8
x=input().split()
print(x[:len(x)-4])

# 11-9
a=input()
b=input()
print(a[1::2]+b[::2])