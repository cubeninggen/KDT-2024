import csv
import matplotlib.pyplot as plt
import koreanize_matplotlib

with open('subwaytime.csv', encoding='utf-8-sig') as f:
    data = csv.reader(f)
    next(data)  # 2줄의헤더정보건너뜀
    next(data)

    station_list=[]
    max_num=1
    max_station=''
    
    for row in data:
        row[4:]=map(int,row[4:])
        passenger_num=sum(row[10:15:2])
        
        station_name=row[3]+'('+row[1]+')'
        station_list.append((station_name,passenger_num))
sorted_passenger_list= sorted(station_list, key=lambda x: x[1], reverse=True)
index=1
for station in sorted_passenger_list[:10]:
    print(f'[{index}]: {station[0]} {station[1]:,}')
    index += 1
station_name, station_passenger= zip(*sorted_passenger_list[:10])
# zip(*리스트):아래for구문과동일기능
# for name, num in sorted_passenger_list[:10]:
#     station_name.append(name)
#     station_passenger.append(num)
plt.figure(figsize=(8, 6))
plt.title('출근시간대승차인원이가장많은10개역', size=16)
plt.bar(range(len(station_passenger)), station_passenger)
plt.xticks(range(len(station_name)), station_name, rotation=70, fontsize=8)
plt.ylabel('승차인원수')
plt.tight_layout() # 최소한의여백생성
plt.show()