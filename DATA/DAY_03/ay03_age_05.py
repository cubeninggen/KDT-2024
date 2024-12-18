import csv
import re
import matplotlib.pyplot as plt
import koreanize_matplotlib
def parse_city_name(city):
    '''
    행정구역명에서도시이름분리(코드번호제거)
    '''
    city_name= re.split('[()]', city)# [0]: 행정구역이름, [1]: 코드번호
    return city_name[0]

def draw_piechart(city_name, city_population, voting_population):
    '''
    전체인구수대비투표가능인구의파이차트작성
    '''
    non_voting_population= city_population-voting_population
    population = [non_voting_population, voting_population]
    color = ['tomato', 'royalblue']
    plt.pie(population, labels=['18세미만', '투표가능인구'], autopct='%.1f%%', colors=color, startangle=90)
    plt.legend()
    plt.title(city_name+ " 투표가능인구비율")
    plt.show()

def get_voting_population(city):
    '''
    투표가능인구수분석row[21:],전체인구수: row[1]
    '''
    f = open('age.csv', encoding='euc_kr')
    data = csv.reader(f)
    header = next(data) # 헤더정보건너뜀
    city_name= ''
    city_population= 0 # 도시전체인구수
    voting_population= 0
    for row in data:
        if city in row[0]:
            city_population= row[1]# 도시전체인구수에서천단위콤마제거
            city_population= city_population.replace(',', '')
            city_population= int(city_population)# (시구동) 이름만분리: 지역번호제거
            city_name= parse_city_name(row[0])
            for data in row[21:]: # 18세이상
                data = data.replace(',','')
                voting_num= int(data)# 누적된투표가능인구수
                voting_population+= voting_num
            break
    f.close()
    print(f'{city_name}전체인구수:{city_population:,}명, 투표가능인구수: {voting_population:,}명')
    draw_piechart(city_name, city_population, voting_population)

city = input('투표가능인구수를확인할도시이름을입력하시오: ')
get_voting_population(city)
