from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup


query=input('(powered by naver)\n검색할 단어 : ')
url= f'https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query={query}'
#response = requests.get(url)
# #soup = BeautifulSoup(response.text, 'html.parser')
 
html = urlopen(url)
soup = BeautifulSoup(html.read(), 'html.parser')
blog_results= soup.select('a.title_link')
print('검색결과수: ', len(blog_results))

for blog_title in blog_results:
    title = blog_title.text
    link = blog_title['href']
    print(f'{title}, [{link}]')