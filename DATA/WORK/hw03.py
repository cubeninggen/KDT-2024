import csv
import matplotlib.pyplot as plt
import koreanize_matplotlib
f = open('gender.csv', encoding='euc_kr')
data = csv.reader(f)
population=[]   # Pie chart에넣을데이터(남, 여인구수)
city = input('찾고싶은지역의이름을입력하세요: ')
male_count= 0
female_count= 0

for row in data:
    if city in row[0]:
        male_count= int(row[104].replace(',', ''))  # 자리수문자열제거및숫자로변환
        female_count= int(row[207].replace(',', ''))
        break  # 도시별하위목록이많음. 처음에나오는데이터가전체총합
print(f'{city}남자인구수: {male_count:,}명, 여자인구수: {female_count:,}명')

population = [male_count, female_count]
color = ['cornflowerblue', 'tomato']
plt.pie(population, labels=['남', '여'], autopct='%.1f%%', colors=color, startangle=90)
plt.title(city + " 남녀성별비율")
plt.show()