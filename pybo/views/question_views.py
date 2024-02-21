from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question
from pybo.forms import QuestionForm, AnswerForm
from pybo.views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question') # main: bp별칭 , __name__: 모듈명 즉, main_views가 인수로 전달

@bp.route('/list/')
def _list():
  page = request.args.get('page', type=int, default=1) # 페이지
  question_list = Question.query.order_by(Question.create_date.desc())
  question_list = question_list.paginate(page=page, per_page=10)
  return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
  form = AnswerForm()
  question = Question.query.get_or_404(question_id)
  return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
  form = QuestionForm()
  if request.method == 'POST' and form.validate_on_submit():
    question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
    db.session.add(question)
    db.session.commit()
    return redirect(url_for('main.index'))
  return render_template('question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
  question = Question.query.get_or_404(question_id)
  if g.user != question.user:
    flash('수정권한이 없습니다.')
    return redirect(url_for('question.detail', question_id=question_id))
  if request.method == 'POST':
    form = QuestionForm()
    if form.validate_on_submit(): #  QuestionForm을 검증하고 아무 이상이 없으면 변경된 데이터를 저장
      form.populate_obj(question) # form 변수에 들어 있는 데이터(화면에서 입력한 데이터)를 question 객체에 업데이트
      question.modify_date = datetime.now()
      db.session.commit()
      return redirect(url_for('question.detail', question_id=question_id))
  else:
    form = QuestionForm(obj=question) # question_id에 해당하는 질문데이터를 갖음
  return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
  question = Question.query.get_or_404(question_id)
  if g.user != question.user:
    flash('삭제권한이 없습니다.')
    return redirect(url_for('question.detail', question_id=question_id))
  db.session.delete(question)
  db.session.commit()
  return redirect(url_for('question._list'))

@bp.route('/vote/<int:question_id>/')
@login_required
def vote(question_id):
  question = Question.query.get_or_404(question_id)
  if g.user == question.user:
    flash('본인이 작성한 글은 추천할 수 없습니다.')
  else:
    question.voter.append(g.user)
    db.session.commit()
  return redirect(url_for('question.detail', question_id=question_id))