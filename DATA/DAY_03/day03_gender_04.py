import csv
import matplotlib.pyplot as plt
import platform
import koreanize_matplotlib
f = open('gender.csv', encoding='euc_kr')
data = csv.reader(f)
city_list= ['서울특별시', '부산광역시','대구광역시', '인천광역시', '광주광역시', '대전광역시' ]
for city in city_list:
    male_list= [] # 리스트데이터초기화
    female_list= [] # 리스트데이터초기화
    for row in data:
        if city in row[0]:
            for i in range(106, 207):# 남여연령대별인구수
                male_list.append(int(row[i].replace(',','')))
                female_list.append(int(row[i+103].replace(',','')))
            break  # 도시하위목록이많음.

    color = ['cornflowerblue', 'tomato']
    plt.plot(male_list, label='남성', color=color[0])
    plt.plot(female_list, label='여성', color=color[1])
    plt.title(city + " 남녀인구수비교")
    plt.xlabel('나이')
    plt.ylabel('인구수')
    plt.legend()
    plt.savefig('img/' + city + '.png', dpi=100)
    plt.close()