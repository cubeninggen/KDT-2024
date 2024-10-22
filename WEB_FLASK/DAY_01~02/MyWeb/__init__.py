#-----------------------------------------------------------------------------
#Flask 에서 webserver구동파일
# - 파일명 : app.py
#-----------------------------------------------------------------------------
# 모듈로딩
from flask import Flask, render_template

#사용자정의 함수
# create_app이름 변경X!!
def create_app():
    # 전역변수
    # Flask Web Server 인스턴스 생성
    APP=Flask(__name__)
    
    from views import main_view
    APP.register_blueprint(main_view.main_bp)

    return APP
# 조건부 실행
if __name__=='__main__':
    # 웹서버 구동
    app=create_app()
    app.run()