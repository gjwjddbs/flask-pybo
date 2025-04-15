from datetime import datetime

from flask import Blueprint , render_template, request, redirect, url_for, g, flash

from pybo.models import Question

from ..forms import QuestionForm, AnswerForm 

from werkzeug.utils import redirect

from sqlalchemy import func 

from ..import db

from pybo.views.auth_views import login_required # 로그인 데코레이터를 사용하기 위해 import

from ..models import Question, Answer, User, question_voter

bp=Blueprint('question',__name__,url_prefix='/question')

@bp.route('/list/')
def _list():
    #입력 파라미터
    page = request.args.get('page',type=int,default=1) #페이지
    kw = request.args.get('kw',type=str,default='') #검색어
    so = request.args.get('so',type=str,default='recent') #정렬기준

    #정렬
    if so == 'recommend': # 추천순으로 정렬
        sub_query = db.session.query(
            question_voter.c.question_id, func.count('*').label('num_voter')) \
            .group_by(question_voter.c.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query,Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_voter.desc(),Question.create_date.desc())
        
    elif so == 'popular' : #답변이 많은 질문 순으로 정렬
        sub_query = db.session.query(
            Answer.question_id, func.count('*').label('num_answer')) \
                .group_by(Answer.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id==sub_query.c.question_id) \
            .order_by(sub_query.c.num_answer.desc(),Question.create_date.desc())
    
    else: #최근 등록된 질문 순으로 정렬
        question_list = Question.query.order_by(Question.create_date.desc())
        
    #조회
    if kw: #검색어가 있을 경우 질문 제목, 내용, 작성자, 답변 내용, 답변 작성자 항목에서 OR 조건으로 검색
        search='%%{}%%'.format(kw) #검색어를 포함하는 질문을 찾기 위해 %%로 감싸줌

        sub_query = db.session.query(
            Answer.question_id, Answer.content, User.username).join(
                User, Answer.user_id==User.id).subquery()
        
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(
                Question.subject.ilike(search) | # 제목
                Question.content.ilike(search) | # 내용
                User.username.ilike(search) | # 질문 작성자
                sub_query.c.content.ilike(search) | #답변 내용
                sub_query.c.username.ilike(search) #답변 작성자
                ) \
            .distinct() 
        
    # 페이징
    question_list = question_list.paginate(page=page,per_page=10)
    return render_template('question/question_list.html',
                           question_list=question_list,page=page,kw=kw)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form=AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html',question=question,form=form)

#질문 등록 함수
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

#질문 수정 함수
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

#질문 삭제 함수
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