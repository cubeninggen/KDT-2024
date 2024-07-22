#----------------------------------------------------------------------------
# Serise/DataFrame에서 사용되는 사용자 덩의 함수들
#---------------------------------------------------------------------------
# 함수의 기능 : DF의 기본정보 와 속성확인
# 함수이름 : checkDF
# 매게변수 : DF인스턴스 변수명, DF인스턴스 이름
# 반환값없음
def checkDF(DF,DFname):
    print(f'[{DFname}]')
    DF.info()
    print(f'[Index]   : {DF.index}')
    print(f'[Columns] : {DF.columns}')
    print(f'[NDim]    : {DF.ndim}')