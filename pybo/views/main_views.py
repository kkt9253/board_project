from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/') # main: bp별칭 , __name__: 모듈명 즉, main_views가 인수로 전달

@bp.route('/hello')
def hello_pybo():
  return 'Hello, pybo!'

@bp.route('/')
def index():
  # question_views.py의 'question'블루프린트의 _list 함수로 리다이렉트
  # redirect(URL): URL로 페이지를 이동 , url_for(라우팅 함수명): 라우팅 함수에 매핑되어 있는 URL을 리턴
  return redirect(url_for('question._list'))