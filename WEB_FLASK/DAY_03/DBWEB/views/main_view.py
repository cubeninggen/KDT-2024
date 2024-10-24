# ------------------------------------------------------------------------------------------
# Flask Framework에서 모듈단위 URL처리 파일
# - 파일명 : main_views.py
# ------------------------------------------------------------------------------------------
# 모듈 로딩 ---------------------------------------------------------------------------------
from flask import Blueprint, render_template
from DBWEB.models.models import Question

#Blueprint 인스턴스 생성
mainBP=Blueprint('MAIN',import_name=__name__,url_prefix='/',template_folder='templates')

# 라우팅함수 정의
@mainBP.route('/')
def index():
    return render_template('index.html',name='홍길동')

@mainBP.route('/qlist')
def printList():
    q_list=Question.query.all()
    return render_template('question_list.html',question_list=q_list)

@mainBP.route('/detail/<int:question_id>/')
def detail(question_id):
    question=Question.query.get(question_id)
    return render_template('question/question_detail.html',question=question)
    