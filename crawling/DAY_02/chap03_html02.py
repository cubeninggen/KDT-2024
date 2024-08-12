from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
soup = BeautifulSoup(html, "html.parser")

# 등장인물의이름: 녹색
name_list= soup.find_all('span', {'class': 'green'})
for name in name_list:
    print(name.string)


# find_all(string=“검색어”)
# 대소문자구분
# 검색어:‘the prince’
prince_list= soup.find_all(string='the prince')
print(prince_list)
print('the prince count: ', len(prince_list))