import os

#ORM 설정 파일

BASE_DIR = os.path.dirname(__file__)

#SQLALCHEMY_DATABASE_URI는 데이터베이스 접속 주소
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))

#SQLALCHEMY 이벤트 처리 옵션
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY="dev"