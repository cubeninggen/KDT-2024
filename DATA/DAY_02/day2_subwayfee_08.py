import csv
import matplotlib.pyplot as plt
import koreanize_matplotlib

label = ['유임승차', '유임하차', '무임승차', '무임하차']
color_list= ['#00ffff', '#ff00bb', '#00ff55', '#ddff00'] # 파이차트컬러값
pic_count= 0
with open('subwayfee.csv', encoding='utf-8-sig') as f:
    data = csv.reader(f)
    next(data)
    for row in data:
        for i in range(4, 8):
            row[i] = int(row[i])
        print(row)
        plt.figure(dpi=100) # 저장할그림파일의dpi 설정
        plt.title(row[3] + ' ' + row[1])
        plt.pie(row[4:8], labels=label, colors=color_list, autopct= '%.1f%%', shadow=True)
        plt.savefig('img/' + row[3] + ' ' + row[1] + '.png')
        plt.close() # 파일닫기
        
        pic_count+= 1
        if pic_count>= 10:
            break