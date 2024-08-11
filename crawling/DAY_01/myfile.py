from bs4 import BeautifulSoup

# 로컬 파일 경로 지정
file_path = r'C:\Users\KDP-48\Desktop\temp_repo-main\temp_repo-main\templates\index.html'

# 파일을 읽고 BeautifulSoup으로 파싱
with open(file_path, 'r', encoding='utf-8') as html_file:
    bs = BeautifulSoup(html_file.read(), 'html.parser')

# HTML 전체 출력
print(bs)
# 첫 번째 <h1> 태그 출력
print(bs.h1)
# 첫 번째 <h1> 태그 안의 문자열 출력
print(bs.h1.string)
