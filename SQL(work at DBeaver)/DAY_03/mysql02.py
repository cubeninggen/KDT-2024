import pymysql

conn = pymysql.connect(host='localhost', user='cube', password='1234',db= 'sakila', charset='utf8')
cur = conn.cursor()

query = """
select c.email
from customer as c
    inner join rental as r
    on c.customer_id= r.customer_id
where date(r.rental_date) = (%s)"""

cur.execute(query, ('2005-06-14'))
rows = cur.fetchall() # 모든데이터를가져옴
for row in rows:
    print(row)
    
cur.close()
conn.close()