from datetime import datetime

from flask import Blueprint , render_template, request, redirect, url_for, g, flash

from pybo.models import Question

from ..forms import QuestionForm, AnswerForm 

from werkzeug.utils import redirect

from ..import db

from pybo.views.auth_views import login_required # 로그인 데코레이터를 사용하기 위해 import

bp=Blueprint('question',__name__,url_prefix='/question')

@bp.route('/list/')
def _list():
    #페이징 기능 추가
    page=request.args.get('page',type=int,default=1) #페이지
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('question/question_list.html',question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form=AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html',question=question,form=form)

@bp.route('/create/', methods=('GET','POST'))
@login_required #로그인 애너테이션 적용, 로그인 여부 확인
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit(): #폼 데이터의 정합성 검사
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index')) #POST 방식이면 데이터 저장, 데이터 저장이 완료되면 main.index로 리다이렉트
    return render_template('question/question_form.html',form=form) # GET 방식으면 질문 등록 페이지 렌더링

#질문 수정
@bp.route('/modify/<int:question_id>',methods=('GET','POST'))
@login_required #질문 수정 시 로그인 여부 확인
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정 권한이 없습니다.') # 수정 권한이 없을 경우 오류 메시지 출력
        return redirect(url_for('question.detail',question_id=question_id))
    if request.method == 'POST': #POST 방식이면 질문 수정 처리
        form  = QuestionForm()
        if form.validate_on_submit(): #폼 데이터의 검증
            form.populate_obj(question) #form의 데이터를 question 객체에 저장
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail',question_id=question_id))
    else:
        form = QuestionForm(obj=question)# 데이터베이스에서 조회한 질문 객체를 obj로 설정하여 폼에 초기값을 설정
    return render_template('question/question_form.html',form=form) #GET 방식이면 질문 수정 페이지 렌더링

#질문 삭제
@bp.route('/delete/<int:question_id>')
@login_required #질문 삭제 시 로그인 여부 확인
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제 권한이 없습니다.') # 삭제 권한이 없을 경우 오류 메세지 출력
        return redirect(url_for('quetion.detail',question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))