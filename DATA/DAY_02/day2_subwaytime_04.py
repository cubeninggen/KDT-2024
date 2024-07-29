import csv
import matplotlib.pyplot as plt
import platform
import koreanize_matplotlib
with open('subwaytime.csv', encoding='utf-8-sig') as f:
    data = csv.reader(f)
    next(data)
    next(data)
    max =[0] * 23 # 새벽3시는지하철운행안함
    max_station= [''] * 23
    xtick_list= []
    for i in range(4, 27):
        n = i% 24
        xtick_list.append(str(n))
    for row in data:
        row[4:] = map(int, row[4:])
        for j in range(23):
            a = row[j * 2 + 4]  # j=0: data[0*2+4]의값을max[0]에저장하기위함
            if a > max[j]:
                max[j] = a
                max_station[j] = xtick_list[j] + '시:' + row[3]+'('+row[1]+')' # 4시: 구로
    for i in range(len(max)):
        print(f'[{max_station[i]}]: {max[i]:,}')
plt.figure(figsize=(10, 10))
plt.title('시간대별최대승차역정보')
plt.bar(range(23), max)
plt.xticks(range(23), labels=max_station, rotation=80)
plt.tight_layout()
plt.show()