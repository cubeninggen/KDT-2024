## [1] outer=5, inner =5

## [2] 대각선 * 출력
# *
#  *
#   *
#    *
#     *
for i in range(5):
    for j in range(i+1):
        print('*' if j==i else ' ',end='\n' if j==i else '')