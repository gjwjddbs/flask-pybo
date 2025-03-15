from datetime import datetime

from flask import Blueprint , render_template, request, redirect, url_for

from pybo.models import Question

from ..forms import QuestionForm, AnswerForm 

from werkzeug.utils import redirect

from ..import db

bp=Blueprint('question',__name__,url_prefix='/question')

@bp.route('/list/')
def _list():
    question_list = Question.query.order_by(Question.create_date.desc())
    return render_template('question/question_list.html',question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form=AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html',question=question,form=form)

@bp.route('/create/', methods=('GET','POST'))
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit(): #폼 데이터의 정합성 검사
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index')) #POST 방식이면 데이터 저장, 데이터 저장이 완료되면 main.index로 리다이렉트
    return render_template('question/question_form.html',form=form) # GET 방식으면 질문 등록 페이지 렌더링