from flask import Blueprint, render_template

from pybo.models import Question

bp = Blueprint('question', __name__, url_prefix='/') # main: bp별칭 , __name__: 모듈명 즉, main_views가 인수로 전달

@bp.route('/list/')
def _list():
  question_list = Question.query.order_by(Question.create_date.desc())
  return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
  question = Question.query.get_or_404(question_id)
  return render_template('question/question_detail.html', question=question)