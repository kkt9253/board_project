from pybo import db

# 모델 클래스는 db.Model 클래스를 상속하여 만들어야 함 - 이때 사용한 db객체는 __init__.py에서 생성한 SQLAlchemy클래스의 객체
class Question(db.Model): # Question 모델을 통해 테이블이 생성되면 테이블명은 question이 됨
  id = db.Column(db.Integer, primary_key=True)
  subject = db.Column(db.String(200), nullable=False)
  content = db.Column(db.Text(), nullable=False)
  create_date = db.Column(db.DateTime(), nullable=False)

class Answer(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  # db.ForeignKey의 'question.id'는 question 테이블의 id 컬럼 의미 즉, Answer 모델의 question_id 속성은 question 테이블의 id 컬럼과 연결 , ondelete='CASCADE'는 질문을 삭제하면 해당 질문에 달린 답변도 함께 삭제
  question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
  # db.relationship를 사용하면 answer.question.subject처럼 참조 가능 , 어떤 질문에 해당하는 객체가 a_question이라면 a_question.answer_set와 같은 코드로 해당 질문에 달린 답변들을 참조 가능
  question = db.relationship('Question', backref=db.backref('answer_set'))
  content = db.Column(db.Text(), nullable=False)
  create_date = db.Column(db.DateTime(), nullable=False)