import requests
from bs4 import BeautifulSoup
import collections

collections.Callable= collections.abc.Callable

url = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0'  # 코스피 상위 10개 기업 정보 페이지 URL
html = requests.get(url)

# 인코딩을 명시적으로 설정
html.encoding = 'euc-kr'

soup = BeautifulSoup(html.text, 'html.parser')

# 기업 이름과 URL을 추출하여 리스트에 저장
company_list = []
company_tags = soup.select('a.tltle')

# 상위 10개 기업만 선택
for tag in company_tags[:10]:
    name = tag.text
    link = 'https://finance.naver.com' + tag['href']
    company_list.append((name, link))

# 메뉴에서 기업 선택 후 상세 정보 출력
while True:
    print("\n-------------------------------------")
    print("[ 네이버 코스피 상위 10대 기업 목록 ]")
    print("-------------------------------------")
    for idx, (name, link) in enumerate(company_list, 1):
        print(f"[ {idx} ] {name}")

    choice = int(input("주가를 검색할 기업의 번호를 입력하세요 (-1: 종료): "))
    
    if choice == -1:
        break

    if 1 <= choice <= 10:
        selected_company = company_list[choice - 1]
        selected_url = selected_company[1]

        # 선택한 기업의 세부 정보를 가져옴
        detail_html = requests.get(selected_url)
        detail_html.encoding = 'euc-kr'
        detail_soup = BeautifulSoup(detail_html.text, 'html.parser')

        # 예시로 특정 정보를 출력
        name = selected_company[0]
        code = selected_url.split('=')[-1]
        current_price = detail_soup.select_one('p.no_today .blind').text.strip()
        prev_price = detail_soup.select('table.no_info .blind')[0].text.strip()
        opening_price = detail_soup.select('table.no_info .blind')[1].text.strip()
        high_price = detail_soup.select('table.no_info .blind')[2].text.strip()
        low_price = detail_soup.select('table.no_info .blind')[3].text.strip()

        print(f"\n종목명: {name}")
        print(f"종목코드: {code}")
        print(f"현재가: {current_price}")
        print(f"전일가: {prev_price}")
        print(f"시가: {opening_price}")
        print(f"고가: {high_price}")
        print(f"저가: {low_price}")
    else:
        print("잘못된 입력입니다. 다시 입력하세요.")
