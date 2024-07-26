import csv
import matplotlib.pyplot as plt
import platform
import koreanize_matplotlib
def draw_lowhigh_graph(start_year, month, day):
    f = open('daegu-utf8.csv', encoding='utf-8-sig')
    data = csv.reader(f)
    next(data)
    high_temp= []  # 최고기온을저장할리스트
    low_temp= []   # 최저기온을저장할리스트
    x_year= []     # x축연도를저장할리스트
    for row in data :
        if row[-1] != '' :
            date_string= row[0].split('-') # 날짜데이터를미리분리함
            if int(date_string[0]) >= start_year: # 문자열값을int형으로변환해서비교
                if int(date_string[1]) == month and int(date_string[2]) == day:
                    high_temp.append(float(row[-1]))
                    low_temp.append(float(row[-2]))
                    x_year.append(date_string[0]) # 연도저장
    f.close()
    plt.figure(figsize=(20, 4))
    plt.plot(x_year, high_temp, 'hotpink', marker='o', label='최고기온') # 최고기온그래프
    plt.plot(x_year, low_temp, 'royalblue', marker='s', label='최저기온') # 최저기온그래프
    # if platform.system() == 'Windows':
    #     plt.rc('font', family='MalgunGothic', size=8) # 간단히맑은고딕으로설정
    # else:plt.rc('font', family='AppleGothic', size=8) # 한글폰트사용For Mac OS
    plt.rcParams['axes.unicode_minus'] = False # 음수(-)가깨지는것방지
    plt.title(f"{start_year}년이후{month}월{day}일의온도변화그래프", size=16)
    plt.legend(loc=2)
    plt.xlabel('year')
    plt.ylabel('temperature')
    plt.show()
draw_lowhigh_graph(2000, 7, 26)