from flask import Flask
app = Flask(__name__) # 애플리케이션 생성

@app.route('/')
def hello():
  return 'hello!!'