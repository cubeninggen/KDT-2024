html_example= '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BeautifulSoup활용</title>
</head>
<body>
    <h1 id="heading">Heading 1</h1>
    <p>Paragraph</p>
    <span class="red">BeautifulSoupLibrary Examples!</span>
    <div id="link">
        <a class="external_link" href="www.google.com">google</a>
        <div id="class1">
            <p id="first">class1's first paragraph</p>
            <a class="external_link" href="www.naver.com">naver</a>
            
            <p id="second">class1's second paragraph</p>
            <a class="internal_link" href="/pages/page1.html">Page1</a>
            <p id="third">class1's third paragraph</p>
        </div>
    </div>
    <div id="text_id2">
        Example page
        <p>g</p>
    </div>
    <h1 id="footer">Footer</h1>
</body>
</html>'''
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_example, 'html.parser')
print(soup.title) # <title> 태그전체를가져옴
print(soup.title.string) # <title>태그의텍스트만리턴
print(soup.title.get_text()) # .string, .text(예전버전)와동일한기능

print(soup.title.parent)

print(soup.body)

print(soup.h1)
print(soup.h1.string)

print(soup.a)             # <a> 태그전체추출:<a class="external_link" href="www.google.com">google</a>
print(soup.a.string)      # <a> 태그내부의텍스트추출(google)
print(soup.a['href'])     # <a> 태그내부의href속성의url을추출
print(soup.a.get('href')) # soup.a['href']와동일기능

print(soup.find('div'))

print(soup.find('div', {'id': 'text_id2'}))
div_text= soup.find('div', {'id': 'text_id2'})
print(div_text.text)
print(div_text.string) # None 리턴

href_link= soup.find('a', {'class': 'internal_link'}) # 딕셔너리형태
href_link= soup.find('a', class_='internal_link') # class_사용: class는파이썬예약어

print(href_link)             # <a class="internal_link", ...>
print(href_link['href'])     # <a>태그내부href속성의값(url)을추출
print(href_link.get('href')) # ['href']와동일기능
print(href_link.text)        # <a> Page1 </a>태그내부의텍스트(Page1) 추출

print('href_link.attrs: ', href_link.attrs) # <a>태그내부의모든속성출력
print('class 속성값: ', href_link['class']) # class 속성의value 출력

print('values():', href_link.attrs.values()) # 모든속성들의값출력

values = list(href_link.attrs.values()) # dictionary 값들을리스트로변경
print(f'values[0]: {values[0]}, values[1]: {values[1]}')

href_value= soup.find(attrs={'href' : 'www.google.com'})
href_value= soup.find('a', attrs={'href': 'www.google.com'})

print('href_value: ', href_value)
print(href_value['href'])
print(href_value.string)

span_tag= soup.find('span')

print('span tag:', span_tag)
print('attrs:', span_tag.attrs)
print('value:', span_tag.attrs['class'])
print('text:', span_tag.text)

# 모든div 태그를검색(리스트형태로반환)
div_tags= soup.find_all('div')
print('div_tagslength: ', len(div_tags))

for div in div_tags:
    print('-----------------------------------------------')
    print(div)

links = soup.find_all('a')

for alink in links:
    print(alink)
    print(f"url:{alink['href']}, text: {alink.string}")
    print()

link_tags= soup.find_all('a', {'class':['external_link', 'internal_link']})
print(link_tags)

p_tags= soup.find_all('p', {'id':['first', 'third']})
for p in p_tags:
    print(p)

head = soup.select_one('head')
print(head)
print('head.text:', head.text.strip())

h1 = soup.select_one('h1') # 첫번째<h1>태그선택
print(h1)

# <h1>태그의id가"footer＂인항목추출
footer = soup.select_one('h1#footer')
print(footer)

class_link= soup.select_one('a.internal_link')
print(class_link)

print(class_link.string)
print(class_link['href'])

# 계층적접근
link1 = soup.select_one('div#link > a.external_link')
print(link1)

link_find= soup.find('div', {'id': 'link'})

external_link= link_find.find('a', {'class': 'external_link'})
print('find external_link: ', external_link)

link2 = soup.select_one('div#class1 p#second')
print(link2)
print(link2.string)

internal_link= soup.select_one('div#link a.internal_link')
print(internal_link['href'])
print(internal_link.text)

h1_all = soup.select('h1')
print('h1_all: ', h1_all)

# html문서의모든<a> 태그의href값추출
url_links= soup.select('a')
for link in url_links:
    print(link['href'])

div_urls= soup.select('div#class1 > a')
print(div_urls)
print(div_urls[0]['href'])

div_urls2 = soup.select('div#class1 a')
print(div_urls2)

# <h1 id="heading”>과<h1 id="footer”> 항목가져오기
h1 = soup.select('#heading, #footer')
print(h1)

url_links= soup.select('a.external_link, a.internal_link')
print(url_links)