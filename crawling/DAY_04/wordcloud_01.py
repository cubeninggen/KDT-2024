from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
import platform 
import numpy as np
from PIL import Image

text = open('test.txt', encoding='utf-8').read()
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
tags = counts.most_common(50)
print(tags)

# 한글을분석하기위해font를한글로지정, macOS는.otf, window는.ttf파일의위치를지정
if platform.system() == 'Windows':
    path = r'c:\Windows\Fonts\malgun.ttf'
elif platform.system() == 'Darwin': # Mac OS
    path = r'/System/Library/Fonts/AppleGothic'
else:
    font = r'/usr/share/fonts/truetype/name/NanumMyeongjo.ttf'

img_mask= np.array(Image.open('cloud.png'))
wc= WordCloud(font_path=path, width=400, height=400,background_color="white", max_font_size=200,repeat=True,colormap='inferno', mask=img_mask)
cloud = wc.generate_from_frequencies(dict(tags))
# 생성된WordCloud를test.jpg로보낸다.
# #cloud.to_file('test.jpg')
plt.figure(figsize=(10, 8))
plt.axis('off')
plt.imshow(cloud)
plt.show()