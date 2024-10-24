#-----------------------------------------------------------------------------
#Flask 에서 webserver구동파일
# - 파일명 : app.py
#-----------------------------------------------------------------------------
# 모듈로딩
from flask import Flask
import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

DB=SQLAlchemy()
MIGRATE=Migrate()

#사용자정의 함수
# create_app이름 변경X!!
def create_app():
    # 전역변수
    # Flask Web Server 인스턴스 생성
    APP=Flask(__name__)

    # DB 관련 초기화 설정
    APP.config.from_object(config)

    # DB 초기화 및 연동
    DB.init_app(APP)
    MIGRATE.init_app(APP,DB)

    # DB 클레스 정의 모듈 로딩
    from .models import models

    # URL 처리 모듈 등록
    from.views import main_view, answer_views
    APP.register_blueprint(main_view.mainBP)
    APP.register_blueprint(answer_views.bp)

    return APP