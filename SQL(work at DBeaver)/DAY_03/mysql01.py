import pymysql
import pandas as pd
import pymysql.cursors
conn = pymysql.connect(host='localhost', user='cube', password='1234',db= 'sakila', charset='utf8')

cur= conn.cursor(pymysql.cursors.DictCursor)
cur.execute('select * from language')
rows = cur.fetchall() # 모든데이터를가져옴
#print(rows)

language_df= pd.DataFrame(rows) 
print(language_df)
print(language_df['name'])
cur.close()
conn.close() # 데이터베이스연결종료