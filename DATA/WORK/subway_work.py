import csv
import matplotlib.pyplot as plt
import koreanize_matplotlib

with open('subwaytime.csv', encoding='utf-8-sig') as f:
    data = csv.reader(f)
    next(data)  # 2줄의헤더정보건너뜀
    next(data)

    print(data[11])
    print(data[14])