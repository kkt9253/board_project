from flask import Flask

def create_app(): # 애플리케이션 팩토리 -> 해당 이름만 정상작동
  app = Flask(__name__)
  
  from .views import main_views
  app.register_blueprint(main_views.bp)
  
  return app