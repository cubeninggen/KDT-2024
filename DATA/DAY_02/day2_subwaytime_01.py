import csv

result = []
total_number= 0
with open('subwaytime.csv', encoding='utf-8-sig') as f:
    data = csv.reader(f)
    next(data) # 2줄의헤더정보를건너뜀
    next(data)
    for row in data:
        row[4:] = map(int, row[4:]) # 문자열을숫자로변경후원래의위치에저장
        total_number+= row[4]
        result.append(row[4])# 새벽4시승차인원을result리스트에추가
print(f'총지하철역의수: {len(result)}')
print(f'새벽4시승차인원: {total_number:,}')