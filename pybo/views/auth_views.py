from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

bp=Blueprint('auth',__name__,url_prefix='/auth')

# 회원가입
@bp.route('/signup/',methods=('GET','POST'))
def signup():
    form = UserCreateForm()
    if request.method=='POST' and form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,password=generate_password_hash(form.password1.data),email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html',form=form)

# 로그인
@bp.route('/login/',methods=('GET','POST'))
def login():
    form = UserLoginForm()
    if request.method =='POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first() # 사용자 이름으로 데이터베이스에서 사용자 정보를 조회
        if not user:
            error = "존재하지 않은 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id']=user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html',form=form)

#로그인 확인
@bp.before_app_request #before_app_request 데코레이터는 사용자 요청이 처리되기 전에 실행되는 함수를 등록할 때 사용
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None #g 객체는 플라스크가 제공하는 컨텍스트 변수로, 요청과 응답이 유효한 동안에만 데이터를 저장하고 유지
    else:
        g.user = User.query.get(user_id)

#로그아웃
@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))