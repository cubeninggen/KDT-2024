from urllib.request import urlopen
from bs4 import BeautifulSoup
import re 

html = urlopen('http://www.pythonscraping.com/pages/page3.html')
soup = BeautifulSoup(html, 'html.parser')

# 정규식: ('img.*\.jpg'): img다음에임의의한문자가0회이상
# -img.jpg, img1.jpg, imga.jpg등
img_tag= re.compile('/img/gifts/img.*.jpg')
# find_all()에서img의src속성값에정규식사용
images = soup.find_all('img', {'src': img_tag}) 
for image in images: 
    print(image, end=" -> ['src'] 속성값: ")
    print(image['src'])