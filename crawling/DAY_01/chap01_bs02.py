from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

try:
    #html= urlopen('http://www.pythonscraping.com/pages/error.html')
    html= urlopen('http://www.pythonscraping.com/pages/page1.html')
except HTTPError as e:
    print(e)
except URLError as e:
    print('The servercouldnotbefound!')
else:
    print('Itworked!')