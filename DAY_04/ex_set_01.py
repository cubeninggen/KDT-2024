#--------------------------------------------------------------------------------------------
# Set자료형 살펴보기
# - 여러 가지 종류의  여러 개 데이터를 저장
# - 단! 중복 안됨!!
# - 컬랙션 타입의 데이터 저장 시 Tuple 가능
# - 형태 : {data1,data2,..., data n}
#--------------------------------------------------------------------------------------------
## [Set 생성]
data=[]
data=()
data={}
data=set()
print(f'data의 타입: {type(data)}, 원소/요소 갯수: {len(data)}, 데이터: {data}')

# 여러개 대이터 저장 : set
data={10,20,30,-90,10,20,30,-90}
print(f'data의 타입: {type(data)}, 원소/요소 갯수: {len(data)}, 데이터: {data}')


data={9.34,'Apple',10,True,'10'}
print(f'data의 타입: {type(data)}, 원소/요소 갯수: {len(data)}, 데이터: {data}')

#data={1,2,3,[1,2,3]} <== [1,2,3] 변경가는한 데이터라 X
#data={1,2,3,(1,2,3)} 
#data={1,2,3,(1)} <== (1)은 중복이라 저장X
data={1,2,3,(1,)[0]}
#data2={1,2,3,data} <== set 또한 변경가능해서 X 
print(f'data의 타입: {type(data)}, 원소/요소 갯수: {len(data)}, 데이터: {data}')

# set() 내장함수
data={1,2,3} # ===> set([1,2,3])
data=set()   # Empty Set
data=set({1,2,3}) #정석적인 형식
data=set([1,2,1,2,3])# type casting
data=set('Good')
data=set({'name':'홍길동','age':12})# key만 가져옴
print(data)

data=list('Good')
print(data)
