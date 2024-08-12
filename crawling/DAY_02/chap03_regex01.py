import re

# compile() 사용안함
m = re.match('[a-z]+', 'Python')
print(m) #‘Python’은대문자로시작하기때문에match()함수의리턴값이None
print(re.search('apple', 'I like apple!'))

# compile() 사용: 객체생성
p = re.compile('[a-z]+') # 알파벳소문자
m = p.match('python')
print(m)
print(p.search('I like apple 123'))

m = re.match('[a-z]+', 'pythoN') # 소문자가1개이상
print(m)

m = re.match('[a-z]+', 'PYthon') # 소문자가1개이상
print(m)

print(re.match('[a-z]+', 'regex python'))
print(re.match('[a-z]+', ' regexpython')) #문자열처음에공백포함

print(re.match('[a-z]+', 'regexpythoN'))
print(re.match('[a-z]+$', 'regexpythoN')) #$:문자열의마지막에소문자1회이상검사

print(re.match('[a-z]+', 'regexPython'))
print(re.match('[a-z]+$', 'regexpython'))

p = re.compile('[a-z]+') # 알파벳소문자
print(p.findall('life is too short! Regularexpression test'))

result = p.search('I like apple 123')
print(result)

result = p.findall('I like apple 123')
print(result)

# ^ .. $ 을명시해야정확한자리수검사가이루어짐
tel_checker= re.compile(r'^(\d{2,3})-(\d{3,4})-(\d{4})$')

print(tel_checker.match('02-123-4567'))
match_groups= tel_checker.match('02-123-4567').groups()
print(match_groups)

print(tel_checker.match('053-950-45678'))
print(tel_checker.match('053950-4567'))

tel_number= '053-950-4567'
tel_number= tel_number.replace('-', '')
print(tel_number)

tel_checker1 = re.compile(r'^(\d{2,3})(\d{3,4})(\d{4})$')
print(tel_checker1.match(tel_number))
print(tel_checker1.match('0239501234')) # 02-3950-1234

tel_checker= re.compile(r'^(\d{2,3})-(\d{3,4})-(\d{4})$')
m = tel_checker.match('02-123-4567')

print(m.groups())
print('group(): ', m.group())
print('group(0): ', m.group(0))
print('group(1): ', m.group(1))
print('group(2,3): ', m.group(2,3))
print('start(): ', m.start()) # 매칭된문자열의시작인덱스
print('end(): ', m.end()) # 매칭된문자열의마지막인덱스+1

cell_phone= re.compile('^(01(?:0|1|[6-9]))-(\d{3,4})-(\d{4})$')

print(cell_phone.match('010-123-4567'))
print(cell_phone.match('019-1234-5678'))
print(cell_phone.match('001-123-4567'))
print(cell_phone.match('010-1234567'))


# 전방긍정탐색: (문자열이won을포함하고있으면won 앞의문자열리턴)
lookahead1 = re.search('.+(?=won)', '1000 won')
if(lookahead1 != None):
    print(lookahead1.group())
else:
    print('None')
lookahead2 = re.search('.+(?=am)', '2023-01-26 am 10:00:01')
print(lookahead2.group())
# 전방부정탐색(?!): 4자리숫자다음에'-'를포함하지않으면앞의문자열리턴
lookahead3 = re.search('\d{4}(?!-)', '010-1234-5678')
print(lookahead3)

# 후방긍정탐색('am' 다음에문자가1개이상있으면, 해당문자열리턴)
lookbehind1= re.search('(?<=am).+', '2023-01-26 am 11:10:01')
print(lookbehind1)
lookbehind2 = re.search('(?<=:).+', 'USD:$51')
print(lookbehind2)

# 후방부정탐색('\b': 공백)
# 공백다음에$기호가없고숫자가1개이상이고공백이있는경우
lookbehind4 = re.search(r'\b(?<!\$)\d+\b', 'I paid $30 for 100 apples.')
print(lookbehind4)