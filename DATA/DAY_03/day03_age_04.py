import csv
import matplotlib.pyplot as plt
import re
import koreanize_matplotlib
def parse_district_name(city):
    '''
    '행정구역' 명칭에서숫자부분을제거함
    -서울특별시종로구(1111000000)
    '''
    city_name= re.split('[()]', city)
    #print(city_name)
    return city_name[0]

def print_population(population):
    '''
    특정지역의인구현황을화면에출력함
    '''
    for i in range(len(population)):
        print(f'{i:3d}세: {population[i]:4d}명', end=' ')
        if (i+ 1) % 10 == 0:
            print()

def draw_population(city_name, population_list):
    '''
    특정지역에대한인구분포를그래프로나타냄(plot)
    -city_name: 지역이름
    -population_list: 0~100세이상까지인구수리스트
    '''
    plt.title(f'{city_name}인구현황')
    plt.xlabel('나이')
    plt.ylabel('인구수')
    plt.bar(range(101), population_list)
    plt.xticks(range(0, 101, 10)) # 0세~ 100세이상
    plt.show()

def get_population(city):
    f = open('age.csv', encoding='euc_kr')
    data = csv.reader(f)
    next(data) # 헤더정보건너뜀
    population_list= []
    full_district_name= ''
    for row in data:
        if city in row[0]:
            full_district_name= parse_district_name(row[0]) # (시구동) 이름만분리: 지역번호제거
            for data in row[3:]:
                data = data.replace(',','') # 천단위콤마제거
                population_list.append(int(data))
            break # 처음으로일치하는도시명만검색하기위함
    f.close()
    print_population(population_list)
    draw_population(full_district_name, population_list)

city = input('인구구조를알고싶은지역의이름(읍면동단위)을입력하세요: ')
get_population(city)