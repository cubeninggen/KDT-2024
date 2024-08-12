import requests
from bs4 import BeautifulSoup
import csv

# 페이지 번호를 포함한 기본 URL
base_url = "https://www.hollys.co.kr/store/korea/korStore2.do?pageNo={}&sido=&gugun=&store="

# 결과를 저장할 파일명
output_file = 'hollys_branches.csv'

# 스크래이핑한 데이터를 저장할 리스트
all_store_info = []

# 1페이지부터 50페이지까지 반복
for page in range(1, 51):
    # 각 페이지에 대한 HTTP GET 요청
    url = base_url.format(page)
    response = requests.get(url)
    
    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # <tbody> 내의 모든 <tr> 태그(행) 추출
    rows = soup.find('tbody').find_all('tr')
    
    # 각 행을 순회하며 필요한 정보 추출
    for row in rows:
        cells = row.find_all('td')
        
        # 원하는 데이터 추출
        region = cells[0].text.strip()        # 첫 번째 <td>: 지역
        store_name = cells[1].text.strip()    # 두 번째 <td>: 매장명
        address = cells[3].text.strip()       # 네 번째 <td>: 주소
        phone_number = cells[5].text.strip()  # 여섯 번째 <td>: 전화번호
        
        # 추출된 데이터를 리스트로 저장
        all_store_info.append([region, store_name, address, phone_number])

# 수집된 데이터를 CSV 파일로 저장
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # CSV 파일의 헤더 작성
    writer.writerow(['지역', '매장명', '주소', '전화번호'])
    
    # 데이터 행 작성
    writer.writerows(all_store_info)

# 화면에 결과 출력
for i, store in enumerate(all_store_info, start=1):
    print(f"[{i:4d}]: 매장이름: {store[1]}, 지역: {store[0]}, 주소: {store[2]}, 전화번호: {store[3]}")

print(f"\n전체 매장 수: {len(all_store_info)}")
print(f"{output_file} 파일 저장 완료")
