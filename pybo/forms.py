from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,PasswordField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired,Length, EqualTo, Email

#질문 등록 폼
class QuestionForm(FlaskForm):
    subject = StringField('제목',validators = [DataRequired('제목은 필수 입력 항목입니다.')])
    content = TextAreaField('내용',validators = [DataRequired('내용은 필수 입력 항목입니다.')])

#답변 등록 폼
class AnswerForm(FlaskForm):
    content=TextAreaField('내용',validators=[DataRequired('내용은 필수 입력 항목입니다.')])

#유저 생성 폼
class UserCreateForm(FlaskForm):
    username = StringField('사용자 이름',validators=[DataRequired(),Length(min=3,max=25)])
    password1 = PasswordField('비밀번호',validators=[DataRequired(),EqualTo('password2','비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호 확인',validators=[DataRequired()])
    email=EmailField('이메일',[DataRequired(),Email()])

#유저 로그인 폼
class UserLoginForm(FlaskForm):
    username = StringField('사용자 이름',validators=[DataRequired(),Length(min=3,max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])

#질문 댓글 폼
class CommentForm(FlaskForm):
    content =TextAreaField('내용',validators=[DataRequired()])