import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib


# 데이터 파일을 읽어옵니다. 
# subwaytime.csv 또는 subway.xls 파일을 사용합니다.
# 파일 경로를 적절히 변경해야 합니다.
file_path = 'subwaytime.csv'  # 또는 'subway.xls'
df = pd.read_csv(file_path, encoding='utf-8-sig')  # 인코딩 문제를 피하기 위해 'cp949' 사용

# 출근 시간대 하차 인원을 계산합니다.
df['하차_07:00-08:59'] = df.iloc[:, 11] + df.iloc[:, 13]

# 필요한 노선 목록
lines = ['1호선', '2호선', '3호선', '4호선', '5호선', '6호선', '7호선']

# 노선별 최대 하차역 정보를 저장할 딕셔너리
max_exit_stations = {}

# 각 노선별로 최대 하차 인원을 찾습니다.
for line in lines:
    line_df = df[df['호선명'] == line]
    max_exit_station = line_df.loc[line_df['하차_07:00-08:59'].idxmax()]
    max_exit_stations[line] = max_exit_station

# 결과 출력
for line, info in max_exit_stations.items():
    station_name = info['지하철역']
    exit_count = info['하차_07:00-08:59']
    print(f"출근 시간대 {line} 최대 하차역: {station_name}역, 하차인원: {exit_count}명")

# 막대그래프를 그립니다.
plt.figure(figsize=(10, 6))
stations = [f"{line} {info['지하철역']}" for line, info in max_exit_stations.items()]
counts = [info['하차_07:00-08:59'] for info in max_exit_stations.values()]

plt.bar(stations, counts, color='skyblue')
plt.xlabel('노선 + 지하철역 이름')
plt.ylabel('하차 인원수')
plt.title('각 노선별 최대 하차역의 출근 시간대 하차 인원')
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
