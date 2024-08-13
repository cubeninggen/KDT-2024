import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parse
import pandas as pd
import collections

if not hasattr(collections, 'Callable'):
    collections.Callable= collections.abc.Callable

html = urlopen('http://en.wikipedia.org/wiki/Comparison_of_text_editors')
bs = BeautifulSoup(html, 'html.parser')

table = bs.find('table', {'class':'wikitable'})
table_data= parse.make2d(table) # 2차원리스트형태로변환

# 테이블의2행을출력
print('[0]:', table_data[0])
print('[1]:', table_data[1])

# Pandas DataFrame으로저장(2행부터데이터저장, 1행은column 이름으로사용)
df= pd.DataFrame(table_data[2:], columns=table_data[1])
print(df.head())

# csv 파일로저장
csvFile= open('editors1.csv', 'w', encoding='utf-8') # t: text mode
writer = csv.writer(csvFile)

for row in table_data:
    writer.writerow(row)
    
csvFile.close()