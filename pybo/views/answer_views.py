from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g
from werkzeug.utils import redirect

from ..forms import AnswerForm

from .. import db 

from ..models import Question, Answer

from .auth_views import login_required # 로그인 데코레이터를 사용하기 위해 import


#answer_views.py 파일이 answer라는 이름의 블루프린트 파일임을 나타냄
bp = Blueprint('answer',__name__,url_prefix='/answer')


@bp.route('/create/<int:question_id>',methods=('POST',))
#답변 저장 템플릿에 있는 form 태그의 action 속성에 해당하는 URL을 나타낸다
@login_required #로그인 애너테이션 적용
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    #name 속성이 content인 form 태그의 데이터를 request.form['content']로 가져온다
    #답변 저장 버튼을 누르면 POST 방식으로 전송되었으면 form.validate_on_submit()이 참이 되어 답변을 저장한다
    if form.validate_on_submit():
        content=request.form['content']
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)
        question.answer_set.append(answer)
        db.session.commit()
        return redirect(url_for('question.detail',question_id=question_id))
    return render_template('question/question_detail.html',question=question,form=form)
