from pybo import db

class Question(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    subject=db.Column(db.String(200),nullable=False)
    content=db.Column(db.Text(),nullable=False)
    create_date=db.Column(db.DateTime(),nullable=False)
    #db.ForeignKey()는 다른 모델과의 관계를 설정하는 역할
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    user=db.relationship('User',backref=db.backref('question_set'))

class Answer(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    question_id=db.Column(db.Integer,db.ForeignKey('question.id',ondelete='CASCADE'))
    #db.backref('answer_set')은 Question 모델에서 Answer 모델을 참조할 수 있도록 하는 역할
    question = db.relationship('Question',backref=db.backref('answer_set',))
    content=db.Column(db.Text(),nullable=False)
    create_date=db.Column(db.DateTime(),nullable=False)
    
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(150),unique=True,nullable=False)
    password=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    