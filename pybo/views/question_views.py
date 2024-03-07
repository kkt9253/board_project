from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from sqlalchemy import func

from pybo import db
from pybo.models import Question, Answer, User, answer_voter
from pybo.forms import QuestionForm, AnswerForm
from pybo.views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question') # main: bp별칭 , __name__: 모듈명 즉, main_views가 인수로 전달

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    question_list = Question.query.order_by(Question.create_date.desc())
    # 생성 날짜 기준으로 내림차순으로 정렬
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) |  # 질문제목
                    Question.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw)


@bp.route('/detail/<int:question_id>')
@bp.route('/detail/<int:question_id>/<int:answer_id>')
def detail(question_id, answer_id=None):
  form = AnswerForm()
  question = Question.query.get_or_404(question_id)
  page = request.args.get('page', type=int, default=1)  # 페이지
  sort = request.args.get('sort', 'latest')
  if sort == 'latest':
    answer_list = Answer.query.filter_by(question_id=question_id).order_by(Answer.create_date.desc())
  elif sort == 'popular':
    # 서브쿼리를 사용하여 각 답변에 대한 투표 수를 세고, 이를 기준으로 정렬
    popular_answers_subquery = db.session.query(
        answer_voter.c.answer_id,
        func.count(answer_voter.c.user_id).label('num_voters')
    ).group_by(answer_voter.c.answer_id).subquery()
    # 인기 있는 답변들을 가져오고 투표 수에 따라 정렬
    answer_list = db.session.query(Answer).outerjoin(
        popular_answers_subquery,
        Answer.id == popular_answers_subquery.c.answer_id
    ).filter(Answer.question_id == question_id).order_by(popular_answers_subquery.c.num_voters.desc())
  answer_list = answer_list.paginate(page=page, per_page=3) # 페이징 갯수
  return render_template('question/question_detail.html', question=question, form=form, answer_list=answer_list)

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