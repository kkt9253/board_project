import os

BASE_DIR = os.path.dirname(__file__)

# 데이터베이스 접속주소 - SQLite 사용되고 데이터베이스 파일은 프로젝트 홈 디렉터리 바로 밑에 pybo.db 파일로 저장
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
# SQLAlchemy의 이벤트를 처리하는 옵션
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 실제 서비스 운영할 때는 유추하기 쉽기 때문에 위험함.
SECRET_KEY = "dev"