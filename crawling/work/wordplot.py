from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
import koreanize_matplotlib
import platform 
import numpy as np
from PIL import Image

text = open('saramin.txt', encoding='utf-8').read()
okt= Okt() # Open Korean Text 객체생성

# okt함수를통해읽어들인내용의형태소를분석한다.
sentences_tag= []
sentences_tag= okt.pos(text)

noun_adj_list= []
# tag가명사이거나형용사인단어들만noun_adj_list에넣어준다.
for word, tag in sentences_tag:
    if tag in ['Noun' , 'Adjective']:
        noun_adj_list.append(word)

print(noun_adj_list)
# 가장많이나온단어부터50개를저장한다.
counts = Counter(noun_adj_list)
tags = counts.most_common(10)
print(tags)

# 한글을분석하기위해font를한글로지정, macOS는.otf, window는.ttf파일의위치를지정
if platform.system() == 'Windows':
    path = r'c:\Windows\Fonts\malgun.ttf'
elif platform.system() == 'Darwin': # Mac OS
    path = r'/System/Library/Fonts/AppleGothic'
else:
    font = r'/usr/share/fonts/truetype/name/NanumMyeongjo.ttf'

# tags 리스트를 각각 단어와 빈도로 분리
words, counts = zip(*tags)

# 바플롯 그리기
plt.figure(figsize=(12, 8))
plt.barh(words, counts, color='skyblue')  # 수평 바플롯 생성
plt.xlabel('빈도수')
plt.ylabel('단어')
plt.title('게임개발에서 가장 많이 나온 단어 10개')
plt.gca().invert_yaxis()  # 상위 단어가 위에 오도록 y축 반전
plt.show()