from datetime import datetime

from flask import Blueprint, url_for, render_template, g, request
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import CommentForm
from pybo.models import Question, Comment
from pybo.views.auth_views import login_required

bp = Blueprint('comment',__name__,url_prefix='/comment')

#댓글 등록 함수 생성
@bp.route('/create/question/<int:question_id>',methods=('GET','POST'))
@login_required
def create_question(question_id):
    form = CommentForm()
    question = Question.query.get_or_404(question_id)
    if request.method == 'POST' and form.validate_on_submit():
        comment = Comment(user = g.user,content=form.content.data, create_date=datetime.now(), question=question)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('question.detail',question_id=question_id))
    return render_template('comment/comment_form.html',form=form)