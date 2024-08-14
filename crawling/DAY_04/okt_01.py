from konlpy.tag import Okt
okt= Okt() # Open Korean Text (과거트위터형태소분석기)
text = "마음에 꽂힌 칼한자루 보다 마음에 꽂힌 꽃한송이가 더 아파서 잠이 오지 않는다"

# pos(text): 문장의각품사를태깅
# norm=True: 문장을정규화, stem=True: 어간을추출
okt_tags= okt.pos(text, norm=True, stem=True)
print(okt_tags)

# nouns(text): 명사만리턴
okt_nouns= okt.nouns(text)
print(okt_nouns)