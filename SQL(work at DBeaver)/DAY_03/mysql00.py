import pymysql
import pandas as pd
import csv
conn = pymysql.connect(host='localhost', user='cube', password='1234',db='sakila', charset='utf8')
cur = conn.cursor()
cur.execute('select * from language')

desc = cur.description# 헤더정보를가져옴
for i in range(len(desc)):
    print(desc[i][0], end=' ')
print()

rows = cur.fetchall() # 모든데이터를가져옴
for data in rows:
    print(data)
print()

cur.close()
conn.close() # 데이터베이스연결종료