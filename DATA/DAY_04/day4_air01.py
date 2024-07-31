import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib

# dust.xlsx불러오기
dust = pd.read_excel('dust.xlsx')

# 데이터읽어오기
print(dust.head())
print(tabulate(dust.head(), headers='keys’,tablefmt=‘pretty'))

print(dust.info())

dust.rename(columns={'날짜': 'date', '아황산가스':'so2','일산화탄소':'co', '오존':'o3','이산화질소':'no2'}, inplace=True)
print(tabulate(dust.head(), headers='keys', tablefmt='psql'))

dust['date'] = dust['date'].str[:10]
print(tabulate(dust.head(), headers='keys', tablefmt='psql'))

dust['date'] = pd.to_datetime(dust['date'])
print(dust.dtypes)

dust['year'] = dust['date'].dt.year
dust['month'] = dust['date'].dt.month
dust['day'] = dust['date'].dt.day
print(dust.columns)

dust = dust[['date', 'year', 'month', 'day', 'so2', 'co', 'o3', 'no2', 'PM10', 'PM2.5']]
print(dust.columns)

print('결측치개수확인하기')
print(dust.isna().sum()) # isnull() 동일

print('결측치를포함한데이터출력')
print(dust[dust.isna().any(axis=1)])

print('결측치채우기')
#dust = dust.fillna(method='ffill') # Pandas 2.2.0 이전버전
dust.ffill(inplace=True) # Pandas 2.2.0 이후
print(dust.isnull().sum())

print(dust.iloc[132:134])# 이전결측치index



weather = pd.read_excel('weather.xlsx')
print(tabulate(weather.head(), headers='keys', tablefmt='psql'))

print(weather.info())

weather.drop(['지점', '지점명'], axis=1, inplace=True)
weather.columns= ['date', 'temp', 'wind', 'rain', 'humidity']
print(tabulate(weather.head(), headers='keys', tablefmt='pretty'))

weather['date'] = pd.to_datetime(weather['date'].dt.date)
print(weather.info())
print(weather.head())

print('날씨데이터결측치개수확인하기')
print(weather.isna().sum())

print('날씨데이터에서결측치를포함하는행출력')
print(weather[weather.isna().any(axis=1)])

weather.ffill(inplace=True)
print(weather.isna().sum())

print(weather.iloc[[369, 565, 742]])

print('강수량이0인항목을0.01로변경')
weather['rain'] = weather['rain'].replace(0, 0.01)
print(weather['rain'].value_counts())

print('dust, weather의크기확인')
print('dust.shape', dust.shape)
print('weather.shape', weather.shape)

print(dust.iloc[740:])

print(weather.iloc[740:])

dust.drop(index=743, inplace=True)
print(dust.shape)

print('dust, weather 데이터프레임merge')
merged_df= pd.merge(dust, weather, on='date')
print(merged_df.head())

pd.set_option('display.max_columns', None)# 전체컬럼출력
pd.set_option('display.max_rows', None)# 전체행출력
print(merged_df.corr())

print('미세먼지(PM10)과상관관계분석')
corr= merged_df.corr()
print(corr['PM10'].sort_values(ascending=False)) # 내림차순정렬

merged_df.hist(column=['so2', 'co', 'o3', 'no2', 'PM10','PM2.5', 'temp', 'wind', 'rain', 'humidity'],bins=50, figsize=(20, 15))
plt.show()

plt.figure(figsize=(15, 10))
daygraph= sns.barplot(x='day', y='PM10', data=merged_df)
plt.title("날짜별PM10 농도")
plt.show()

plt.figure(figsize=(15, 10))
sns.heatmap(data=corr, annot=True, fmt='.2f', cmap='hot')
plt.show()

plt.figure(figsize=(15, 10))
x = merged_df['PM10']
y = merged_df['PM2.5']
plt.plot(x, y, marker='o', linestyle='none', color='red', alpha=0.5)
plt.title('PM10 vs. PM2.5')
plt.xlabel('PM10')
plt.ylabel('PM2.5')
plt.show()