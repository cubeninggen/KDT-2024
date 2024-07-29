import random

sticks=[0,0,0,0]
def yut_play():
    for i in range(4):
        sticks[i]=random.randint(0,1)
    yut=sticks
    yut=sum(yut)
    if yut==0:
        return 4
    elif yut==1:
        return 3
    elif yut==2:
        return 2
    elif yut==3:
        return 1
    elif yut==4:
        return 5
point=[0,0]
HorN=0
while point[0]<20 or point[1]<20:
        if point[HorN]==20:
            break
        else:
            point[HorN]+=yut_play()
            if yut_play()==4 or yut_play()==5:
                break
        HorN=1-HorN
print(point[0],point[1])
