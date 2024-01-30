from flask import Flask

def create_app(): # 애플리케이션 팩토리 -> 해당 이름만 정상작동
  app = Flask(__name__)

  @app.route('/')
  def hello_pybo():
    return 'Hello, Pybo!'
  
  return app