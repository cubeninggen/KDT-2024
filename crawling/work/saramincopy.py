from urllib.request import Request, urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
import collections

if not hasattr(collections, 'Callable'):
    collections.Callable = collections.abc.Callable

all_jobs = ""
for i in range(1, 6):
    try:
        search_word = quote('게임개발')
        url = f'https://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=search&recruitPage={i}&recruitSort=reg_dt&recruitPageCount=100&searchword={search_word}'

        urlrequest = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(urlrequest)

        soup = BeautifulSoup(html, 'html.parser')
        content = soup.find('div', {'class': 'content'})
        items = content.find_all('div', {'class': 'job_sector'})

        for item in items:
            # 날짜가 포함된 span 태그를 찾아서 제거
            date_span = item.find('span', {'class': 'job_day'})
            if date_span:
                date_span.decompose()  # 날짜 부분을 제거

            # 정리된 텍스트 추출
            item_string = item.text.replace('\n', '').strip()
            item_string = item.text.replace('외', '').strip()
            item_string = item.text.replace(',', '').strip()
            if item_string.endswith("외"):
                item_string = item_string[:-1].strip()
            all_jobs += item_string + "\n"
            print(item_string)

    except Exception as e:
        print(e)
print()
print(all_jobs)
with open('saramin.txt', 'w', encoding='utf-8') as file:
    file.write(all_jobs)
