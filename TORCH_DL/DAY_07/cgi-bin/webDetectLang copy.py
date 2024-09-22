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

def showHTML(form_data, msg):
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
                        <a href="https://store.steampowered.com/app/359550/Tom_Clancys_Rainbow_Six_Siege/">레인보우식스 시즈 스팀 구매 페이지</a>
                        <a href="https://x.com/rainbow6game"> 레인보우식스 시즈 공식X</a>
                        <a href="https://www.youtube.com/channel/UCj0iColXMAjPA92rH-AXVGQ"> 레인보우식스 공식 유튜브</a>
                        <br>
                        유용한사이트
                        <br>
                        <a href="https://r6.tracker.network//"> 레인보우식스 전적사이트</a>
                </div>
                <hr>
                <div class="mybox">
                    <form method="post">
                        <label>맵 이름:</label><br>
                        <input type="text" name="mapname" value="{form_data.get('mapname', '')}" /><br><br>
                        
                        <label>라운드 수:</label><br>
                        <input type="text" name="roundnumber" value="{form_data.get('roundnumber', '')}" /><br><br>
                        
                        <label>공격/방어 팀:</label><br>
                        <input type="text" name="role" value="{form_data.get('role', '')}" /><br><br>
                        
                        <label>킬 수:</label><br>
                        <input type="text" name="nbkills" value="{form_data.get('nbkills', '')}" /><br><br>

                        <label>사망 여부(0 or 1):</label><br>
                        <input type="text" name="isdead" value="{form_data.get('isdead', '')}" /><br><br>

                        <p><input type="submit" value="승리 예측하기"></p>
                        <p>{msg}</p>
                    </form>
                </div>
            </div>

            <div class="layout">
                <img src="https://lh3.googleusercontent.com/proxy/coZqYVXX4fM06Sf1ETzI_JUtYLIDR_-Z0y7boAyZPTPGK0ZNuCnEVh-w72Z2PjpczI69kOK-z2ONIK_v6UUOYX7y_bxzpx489J5bKTGc2oK5fLfvPvbbqIdIMX5wAodjnnP8Lp4EneAjS1omBO4ewO0h_fMrt3avUbtoyhQ-AEvv7wgQ8-4zSpXhHpmmhJxcXloPOk2FA3256t3zur7aGPgr41nBVA" />
            </div>
        </body>

        </html>""")

# 사용자 입력 데이터를 예측 모델에 전달하여 승률 예측하는 함수 ----------------------------------
def predictWin(form_data):
    try:
        # 사용자 입력을 바탕으로 모델에 전달할 피처 구성
        feature_list = [
            form_data['roundnumber'],
            form_data['nbkills'],
            form_data['isdead'],
            # 추가적인 입력 값을 넣어줌 (예: 맵, 역할 등)
        ]
        
        # 데이터 타입 변환 및 예측
        feature_list = list(map(float, feature_list))  # 모델에 넣기 전에 데이터 타입을 float으로 변환
        prediction = winModel.predict([feature_list])[0]  # 예측값 가져오기
        return "승리" if prediction == 1 else "패배"
    except Exception as e:
        return f"예측 오류: {str(e)}"

# 기능 구현 ------------------------------------------------
# (1) WEB 인코딩 설정
if SCRIPT_MODE:
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())  # 웹에서만 필요 : 표준출력을 utf-8로

# (2) 모델 로딩
if SCRIPT_MODE:
    pklfile = os.path.dirname(__file__) + '/model_R6.pth'  # 예측 모델 경로
else:
    pklfile = './model_R6.pth'

winModel = joblib.load(pklfile)

# (3) WEB 사용자 입력 데이터 처리
form = cgi.FieldStorage()

# (3-2) 입력 값 받아오기
form_data = {
    'mapname': form.getvalue("mapname", ""),
    'roundnumber': form.getvalue("roundnumber", ""),
    'role': form.getvalue("role", ""),
    'nbkills': form.getvalue("nbkills", ""),
    'isdead': form.getvalue("isdead", ""),
}

# (3-3) 판별하기
msg = ""
if all(value != "" for value in form_data.values()):  # 모든 입력 값이 채워졌을 때만 예측 실행
    result = predictWin(form_data)
    msg = f"예측 결과: {result}"

# (4) 사용자에게 WEB 화면 제공
showHTML(form_data, msg)
