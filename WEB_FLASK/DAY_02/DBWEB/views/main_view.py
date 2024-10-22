# ------------------------------------------------------------------------------------------
# Flask Framework에서 모듈단위 URL처리 파일
# - 파일명 : main_views.py
# ------------------------------------------------------------------------------------------
# 모듈 로딩 ---------------------------------------------------------------------------------
from flask import Blueprint, render_template

#Blueprint 인스턴스 생성
mainBP=Blueprint('MAIN',import_name=__name__,url_prefix='/',template_folder='templates')

# 라우팅함수 정의
@mainBP.route('/')
def index():
    return render_template('index.html')