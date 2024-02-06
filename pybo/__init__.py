from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

import config

naming_convention = {
  "ix": 'ix_%(column_0_label)s',
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(column_0_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def create_app(): # 애플리케이션 팩토리 -> 해당 이름만 정상작동
  app = Flask(__name__)
  app.config.from_object(config) # config.py 사용

  # ORM
  db.init_app(app) # init_app 메서드 사용해서 app에 등록
  if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
    migrate.init_app(app, db, render_as_batch=True)
  else:
    migrate.init_app(app, db)  
  from . import models

  # 블루프린트
  from .views import main_views, question_views, answer_views, auth_views
  app.register_blueprint(main_views.bp)
  app.register_blueprint(question_views.bp)
  app.register_blueprint(answer_views.bp)
  app.register_blueprint(auth_views.bp)

  # 필터
  from .filter import format_datetime
  app.jinja_env.filters['datetime'] = format_datetime
  
  return app