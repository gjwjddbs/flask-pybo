from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from markdown import markdown
from markupsafe import Markup

import config

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db=SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    #ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app,db,render_as_batch=True)
    else:
        migrate.init_app(app,db)
    from . import models
    
    #블루 프린트
    from .views import main_views , question_views, answer_views,auth_views, comment_views, vote_views
    #블루 프린트 객체 bp 등록
    app.register_blueprint(main_views.bp) 
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(vote_views.bp)

    #필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    #마크 다운
    # nl2br : 줄 바꿈을 <br>로 바꿔 준다
    # fenced_code : 코드 표시 를 위해 <pre>와 <code> 태그를 사용한다
    @app.template_filter('markdown')
    def markdown_filter(text):
        return Markup(markdown(text,extenstions=['nl2br','fenced_code']))

    return app


 