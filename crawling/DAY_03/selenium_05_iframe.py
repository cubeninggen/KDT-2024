from bs4 import BeautifulSoup
from selenium import webdriver
import collections

collections.Callable= collections.abc.Callable

driver = webdriver.Chrome()  # 본인의webdriver경로
driver.get('https://blog.naver.com/swf1004/221631056531')

driver.switch_to.frame('mainFrame') # 해당iframe으로이동

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

results = soup.find_all('div', {'class': 'se-module'})

result1=[]
for result in results:
    remove_carriage_str= result.text.replace('\n', '')
    print(remove_carriage_str)
    result1.append(remove_carriage_str)