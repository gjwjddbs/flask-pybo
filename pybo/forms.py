from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired 

#질문 등록 폼
class QuestionForm(FlaskForm):
    subject = StringField('제목',validators = [DataRequired('제목은 필수 입력 항목입니다.')])
    content = TextAreaField('내용',validators = [DataRequired('내용은 필수 입력 항목입니다.')])

#답변 등록 폼
class AnswerForm(FlaskForm):
    content=TextAreaField('내용',validators=[DataRequired('내용은 필수 입력 항목입니다.')])

