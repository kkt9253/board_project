from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import CommentForm
from pybo.models import Question, Answer, Comment
from pybo.views.auth_views import login_required

bp = Blueprint('comment', __name__, url_prefix='/comment')

@bp.route('/create/<int:question_id>/<int:answer_id>', methods=('POST',))
@login_required
def create(question_id, answer_id):
  form = CommentForm()
  question = Question.query.get_or_404(question_id)
  answer = Answer.query.get_or_404(answer_id)
  if form.validate_on_submit():
    content = request.form['content']
    comment = Comment(content=content, create_date=datetime.now(), user=g.user, answer_id=answer_id)
    question.comment_question_set.append(comment)
    db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id, answer_id=answer_id))
  return render_template('question/question_detail.html', question=question, answer=answer, form=form)