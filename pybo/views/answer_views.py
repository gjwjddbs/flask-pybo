from datetime import datetime

from flask import Blueprint, url_for, request
from werkzeug.utils import redirect

from pybo import db 

from pybo.models import Question, Answer

#answer_views.py 파일이 answer라는 이름의 블루프린트 파일임을 나타냄
bp = Blueprint('answer',__name__,url_prefix='/answer')


@bp.route('/create/<int:question_id>',methods=('POST',))
#답변 저장 템플릿에 있는 form 태그의 action 속성에 해당하는 URL을 나타낸다
def create(question_id):
    question = Question.query.get_or_404(question_id)
    #name 속성이 content인 form 태그의 데이터를 request.form['content']로 가져온다
    content=request.form['content']
    answer = Answer(content=content,create_date=datetime.now())
    #질문과 답변은 1:N 관계이므로 질문에 답변을 추가하기 위해 append() 메서드를 사용한다
    question.answer_set.append(answer)
    db.session.commmit()
    return redirect(url_for('question.detail',question_id=question_id))
