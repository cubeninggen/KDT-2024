# 위에 라인 : 셀 내용을 파일로 생성/ 한번 생성후에는 마스킹

# 모듈 로딩--------------------------------------------
import os.path     # 파일 및 폴더 관련
import cgi, cgitb  # cgi 프로그래밍 관련
import joblib      # AI 모델 관련
import sys, codecs # 인코딩 관련
from pydoc import html # html 코드 관련 : html을 객체로 처리?

# 동작관련 전역 변수----------------------------------
SCRIPT_MODE = True    # Jupyter Mode : False, WEB Mode : True
cgitb.enable()         # Web상에서 진행상태 메시지를 콘솔에서 확인할수 있도록 하는 기능

# 사용자 정의 함수-----------------------------------------------------------
# WEB에서 사용자에게 보여주고 입력받는 함수 ---------------------------------
# 함수명 : showHTML
# 재 료 : 사용자 입력 데이터, 판별 결과
# 결 과 : 사용자에게 보여질 HTML 코드

def showHTML(text, msg):
    print("Content-Type: text/html; charset=utf-8")
    print(f"""
    
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8" />
            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />

            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
                integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous" />
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
                integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM"
                crossorigin="anonymous"></script>

            <link href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap" rel="stylesheet" />
            <title> RAINBOWSIX SIEGE| 승률 예측</title>

            <meta property="og:title" content="레인보우 식스 시즈 승률 예측" />
            <meta property="og:description" content="레인보우식스 시즈 승률 예측 모델 구동 사이트" />
            <meta property="og:image" content="https://www.kemperlesnik.com/wp-content/uploads/2020/05/rainbow-six-siege-logo-header.-1.jpg" />

            <style>
                .layout {{
                    background-color: #ffffffa6;
                    color: black;
                    text-align: center;
                }}

                .video {{
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    z-index: -1;
                    overflow: hidden;
                    margin: 0 auto;
                    transform: translateX(-50%) translateY(-50%);
                }}

                .mybox {{
                    width: 95%;
                    max-width: 700px;
                    padding: 20px;
                    box-shadow: 0px 0px 10px 0px lightblue;
                    margin: 20px auto;
                }}
            </style>
        </head>

        <body>
            <div class="layout">
                <video class="video" src="https://staticctf.ubisoft.com/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/4GJ98jq8CtE4GFjtWb6G27/87b1545a8a0efc5afa78d74a2802600e/r6s-y9s3-homepage.mp4" muted="muted" loop="loop"
                    playsinline="" autoplay="autoplay"></video>
                <h1><img src="https://staticctf.ubisoft.com/J3yJr34U2pZ2Ieem48Dwy9uqj5PNUQTn/DAwqy5hMljnxm7evA5ASN/e3266cda0a738a3abd486d5f57d732d7/r6s-logo-ww.png" />
                </h1>
                <h2>레인보우식스 시즈 승률 예측 모델 구동 사이트</h2>
                <hr>
                <div>
                    <span style="color:rgb(86, 86, 86)">공식사이트<br>
                        <a href="https://www.ubisoft.com/en-gb/game/rainbow-six/siege"> 레인보우식스 시즈</a>
                        <a href="https://store.steampowered.com/app/359550/Tom_Clancys_Rainbow_Six_Siege/">레인보우식스 시즈 스팀 구매 패이지</a>
                        <a href="https://x.com/rainbow6game"> 레인보우식스 시즈 공식X</a>
                        <a href="https://www.youtube.com/channel/UCj0iColXMAjPA92rH-AXVGQ"> 블루아카이브 공식유튜브</a>
                        <br>
                        유용한사이트
                        <br>
                        <a href="https://r6.tracker.network//"> 레인보우식스 전적사이트</a>
                </div>
                <hr>
                <div>
                    <h1></h1>
                </div>
                <div class="mybox">
                    <form>
                        <textarea name="text" rows="10" colos="40" >{text}</textarea>
                        <p><input type="submit" value="언어감지">{msg}</p>
                    </form>
                </div>
            </div>

            <div class="layout">
                <img
                    src="https://lh3.googleusercontent.com/proxy/coZqYVXX4fM06Sf1ETzI_JUtYLIDR_-Z0y7boAyZPTPGK0ZNuCnEVh-w72Z2PjpczI69kOK-z2ONIK_v6UUOYX7y_bxzpx489J5bKTGc2oK5fLfvPvbbqIdIMX5wAodjnnP8Lp4EneAjS1omBO4ewO0h_fMrt3avUbtoyhQ-AEvv7wgQ8-4zSpXhHpmmhJxcXloPOk2FA3256t3zur7aGPgr41nBVA" />

            </div>
        </body>

        </html>""")

    
# 사용자 입력 텍스트 판별하는 함수---------------------------------------------------------------------------
# 함수명 : detectLang
# 재 료 : 사용자 입력 데이터
# 결 과 : 판별 언어명(영어, 프랑스~)

def detectLang(text):
    # 모든 문자 통일 -> 소문자
    text = text.lower()
    print(f'text=>{text}')
    
    # 문자 1개씩 읽어서 a~z 사이 있는 것만 카운팅
    codeA, codeZ = (ord('a'), ord('z'))
    cnt = [ 0 for n in range(26)]
    print(f'cnt => {cnt}')
    
    for ch in text:
        # 예 : ch가 a인 경우
        print(f'ch=>{ch} :{ord(ch)}')
        if codeA <= ord(ch) <= codeZ:
            cnt[ord(ch)-codeA] += 1
    print(f'cnt=>{cnt}')
    
    # text내의 a~z 빈도 계산
    total = sum(cnt)
    freq = list(map(lambda n: n/total, cnt))
    print(f'freq => {freq}')
    
    # 판별요청 & 결과 반환
    result = langModel.predict([freq])
    langDict = {'en':'영어', 'fr':'프랑스어', 'id': '인도네시아어', 'tl':'타갈로그어'}
    
    return langDict[result[0]]

# 기능 구현 ------------------------------------------------
# (1) WEB 인코딩 설정
if SCRIPT_MODE:
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach()) #웹에서만 필요 : 표준출력을 utf-8로

# (2) 모델 로딩
if SCRIPT_MODE:
    pklfile = os.path.dirname(__file__)+ '/lang.pkl' # 웹상에서는 절대경로만
else:
    pklfile = './lang.pkl'
    
langModel = joblib.load(pklfile)

# (3) WEB 사용자 입력 데이터 처리
# (3-1) HTML 코드에서 사용자 입력 받는 form 태크 영역 객체 가져오기
form = cgi.FieldStorage()

# (3-2) Form안에 textarea 태크 속 데이터 가져오기
text = form.getvalue("text", default="")
#text ="Happy New Year" # 테스트용 (쥬피터 내부)

# (3-3) 판별하기
msg =""
if text != "":
    resultLang = detectLang(text)
    msg = f"{resultLang}"

# (4) 사용자에게 WEB 화면 제공
showHTML(text,msg)
