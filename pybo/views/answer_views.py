from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
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

#답변 수정
@bp.route('/modify/<int:answer_id>',methods=('GET','POST'))
@login_required #답변 수정 시 로그인 여부 확인
def modify(answer_id):
    answer=Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정 권한이 없습니다.')# 답변 수정 권한이 없는 경우 오류 메세지 출력
        return redirect(url_for('question.detail',question_id = answer.quetion.id))
    if request.method == 'POST':
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail',question_id = answer.question.id))
    else:
        form = AnswerForm(obj=answer) #데이터베이스에서 조회한 답변 객체를 obj로 설정하여 폼에 초기값을 설정
    return render_template('answer/answer_form.html',answer=answer,form=form) #GET 방식이면 답변 수정 페이지 렌더링

#답변 삭제
@bp.route('/delete/<int:answer_id>')
@login_required #답변 삭제 시 로그인 여부 확인
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('삭제 권한이 없습니다') #답변 삭제 권한이 없는 경우 오류 메세지 출력
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail',question_id=question_id)) #답변 삭제 후 질문 상세 페이지로 리다이렉트