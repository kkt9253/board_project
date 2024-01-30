from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='/') # main: bp별칭 , __name__: 모듈명 즉, main_views가 인수로 전달

@bp.route('/hello')
def hello_pybo():
  return 'Hello, pybo!'

@bp.route('/')
def index():
  return 'Pybo index'