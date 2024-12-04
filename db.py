from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
# DB 정보
db_host = "dpg-csu2uct6l47c73djpak0-a.oregon-postgres.render.com"
port = 5432
user_name = "database_wvl1_user"
user_pwd = "4RR5vnL2EreOdJkbzVEyiTvhvr1eLsXE"
db_name = "database_wvl1"
# SQLAlchemy의 PostgreSQL 접속 문자열을 생성
DATABASE = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{dbname}".format(
    host=db_host,
    port=port,
    username=user_name,
    password=user_pwd,
    dbname=db_name
)
# create_engine 함수를 사용하여 데이터베이스 엔진을 생성
ENGINE = create_engine(DATABASE)
# scoped_session 함수를 사용하여 스레드로부터 안전한 세션 생성
session = scoped_session(
sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = ENGINE
    )
)
# Base 클래스를 사용하여 모든 ORM 모델의 기본 클래스를 생성합니다.
Base = declarative_base()