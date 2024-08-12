import csv
from tabulate import tabulate

# CSV 파일 경로
csv_file = 'hollys_branches.csv'

def load_store_data(file_path):
    stores = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            stores.append(row)
    return stores

def find_stores_by_region(stores, region):
    result = [store for store in stores if region in store['지역']]
    return result

def display_stores(stores):
    if len(stores) == 0:
        print("검색된 매장이 없습니다.")
    else:
        headers = ["#", "매장이름", "주소", "전화번호"]
        table = [[i + 1, store['매장명'], store['주소'], store['전화번호']] for i, store in enumerate(stores)]
        print(f"검색된 매장 수:\t{len(stores)}")
        print(tabulate(table, headers, tablefmt="grid"))

def main():
    # 저장된 매장 정보를 로드
    stores = load_store_data(csv_file)
    
    while True:
        region = input("검색할 매장의 지역을 입력하세요:")
        
        if region.lower() == 'quit':
            print("종료 합니다.")
            break
        
        # 입력한 지역에 해당하는 매장 검색
        filtered_stores = find_stores_by_region(stores, region)
        
        # 검색된 매장 정보 출력
        display_stores(filtered_stores)

if __name__ == "__main__":
    main()
