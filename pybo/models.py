from pybo import db

#질문 추천 객체
question_voter = db.Table(
    'question_voter',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),primary_key=True),
    db.Column('question_id',db.Integer,db.ForeignKey('question.id',ondelete='CASCADE'),primary_key=True)
)

#답변 추천 객체
answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),primary_key=True),
    db.Column('answer_id',db.Integer,db.ForeignKey('answer.id',ondelete='CASCADE'),primary_key=True)
)

#질문 모델
class Question(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    subject=db.Column(db.String(200),nullable=False)
    content=db.Column(db.Text(),nullable=False)
    create_date=db.Column(db.DateTime(),nullable=False)
    #db.ForeignKey()는 다른 모델과의 관계를 설정하는 역할
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    user=db.relationship('User',backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(),nullable=True)
    voter=db.relationship('User',secondary=question_voter,backref=db.backref('question_voter_set'))

#답변 모델
class Answer(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    question_id=db.Column(db.Integer,db.ForeignKey('question.id',ondelete='CASCADE'))
    #db.backref('answer_set')은 Question 모델에서 Answer 모델을 참조할 수 있도록 하는 역할
    question = db.relationship('Question',backref=db.backref('answer_set',))
    content=db.Column(db.Text(),nullable=False)
    create_date=db.Column(db.DateTime(),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete='CASCADE'),nullable=False)
    user=db.relationship('User',backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(),nullable=True)
    voter=db.relationship('User',secondary=answer_voter,backref=db.backref('answer_voter_set'))
    
#회원가입 모델
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(150),unique=True,nullable=False)
    password=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    
#댓글 모델
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),nullable=False)
    user=db.relationship('User',backref=db.backref('comment_set'))
    content = db.Column(db.Text(),nullable=False)
    create_date = db.Column(db.DateTime(),nullable=False)
    modify_date = db.Column(db.DateTime())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id',ondelete='CASCADE'),nullable=True)
    question = db.relationship('Question',backref=db.backref('comment_set'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id',ondelete='CASCADE'),nullable=True)
    answer = db.relationship('Answer', backref = db.backref('comment_set'))
