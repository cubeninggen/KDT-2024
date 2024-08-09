import pymysql
import pandas as pd
import matplotlib.pyplot as plt

conn = pymysql.connect(host='172.20.145.44', user='cube', password='1234',db= 'mini_project', charset='utf8')
cur = conn.cursor(pymysql.cursors.DictCursor)
dfL=[]
query="""select b.Country,b.dollar_price,g.Year_2022
from bigmacprice as b inner join gdp_data as g
on b.Country=g.Country;"""
cur.execute(query)
rows = cur.fetchall()
for row in rows:
    dfL.append(row)
df1=pd.DataFrame(dfL)
print(df1)

cur.close()
conn.close()
df1['Year_2022'] = df1['Year_2022'].str.replace(',', '').astype(float)
plt.figure(figsize=(20, 10))

# 첫 번째 데이터 (dollar_price)
plt.bar(df1['Country'], df1['dollar_price'], color='b', label='Dollar')
# 두 번째 데이터 (Year_2022)
#plt.bar(df1['Country'], df1['Year_2022'], color='r', label='GDP')

# 제목과 축 레이블 추가
plt.title('Dollar Price and Year 2022 Data')
plt.xlabel('Country')
plt.ylabel('Values')

# x축 레이블을 회전
plt.xticks(rotation=45)

# 범례 추가
plt.legend()
#plt.yticks([])
# 그래프 표시
plt.tight_layout()
plt.show()