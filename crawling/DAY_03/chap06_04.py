import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://en.wikipedia.org/wiki/Comparison_of_text_editors')
bs = BeautifulSoup(html, 'html.parser')
# 두개의테이블중에첫번째테이블사용
table = bs.find_all('table', {'class':'wikitable'})[0]
rows = table.find_all('tr')

csvFile= open('editors.csv', 'wt', encoding='utf-8') # t: text mode
writer = csv.writer(csvFile)
try:
    for row in rows:
        csvRow= []
        for cell in row.find_all(['th', 'td']):
            print(cell.text.strip())
            csvRow.append(cell.text.strip())
            writer.writerow(csvRow)
finally:
    csvFile.close()