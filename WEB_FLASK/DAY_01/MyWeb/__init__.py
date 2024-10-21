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

    # 라우팅 기능 함수
    # @Flask web server 인스턴스 변수명.route("url")
    @APP.route("/")
    def index():
        return render_template("index.html")

    @APP.route("/info")
    @APP.route("/info/")
    def info():
        return'''<iframe src="https://yorha-archive.netlify.app/map" name="html" width="100%" height="100%"></iframe>'''

    @APP.route("/info/<name>")
    def printInfo(name):
        return render_template("info.html",name=name)
    @APP.route("/info/<int:num>")
    def printInt(num):
        return f'''<h1>{num}'s yorha map(num)</h1><hr>
        <iframe src="https://yorha-archive.netlify.app/map" name="html" width="100%" height="100%"></iframe>'''

    @APP.route("/go")
    def goHome():
        return APP.redirect("/info")
    
    return APP
# 조건부 실행
if __name__=='__main__':
    # 웹서버 구동
    app=create_app()
    app.run()