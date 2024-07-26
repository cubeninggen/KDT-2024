import pandas as pd

weather_df= pd.read_csv('daegu-utf8.csv', encoding='utf-8-sig')
print(weather_df.columns)
print(weather_df['날짜'].dtype) # 날짜컬럼은object 타입

weather_df.columns=['날짜', '지점', '평균기온', '최저기온', '최고기온']
print(weather_df.columns)

weather_df['날짜'] = pd.to_datetime(weather_df['날짜'], format='%Y-%m-%d')
print(weather_df['날짜'].dtype)

print(weather_df.head(5))
print(weather_df.shape)
num_rows= weather_df.shape[0] # shape(row, col), shape[0]: row의개수
num_missing= num_rows-weather_df.count() # count(): 정상값의개수
print(num_missing)

weather_df= weather_df.dropna(axis=0)
print(weather_df.count())
print(weather_df.head(5))

weather_df.to_csv('daegu-utf8-df.csv', index=False, mode='w', encoding='utf-8-sig')

print('특정연도와달의최고, 최저기온평균값계산')
year_df= weather_df[weather_df['날짜'].dt.year== 2023]
month_df= year_df[year_df['날짜'].dt.month== 8]
print(month_df.head())

max_temp_mean= round(month_df['최고기온'].mean(), 1)
min_temp_mean= round(month_df['최저기온'].mean(), 1)
print(f'2023년8월최저기온평균:{min_temp_mean}, 최고기온평균:{max_temp_mean}')