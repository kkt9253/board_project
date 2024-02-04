from flask import Blueprint, url_for, render_template, request, flash
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm
from pybo.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth') # main: bp별칭 , __name__: 모듈명 즉, main_views가 인수로 전달

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
  form = UserCreateForm()
  if request.method == 'POST' and form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if not user:
      user = User(username=form.username.data, password=generate_password_hash(form.password1.data), email=form.email.data)
      db.session.add(user)
      db.session.commit()
    else:
      flash('이미 존재하는 사용자입니다.')
  return render_template('auth/signup.html', form=form)