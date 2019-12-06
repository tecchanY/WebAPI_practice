from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

from sqlalchemy.ext.declarative import declarative_base

# データベースエンジン作成とセッション作成。echo=Trueで発行されるSQL文をログに吐く
# ここの1行を書き換えるだけでMySQLやSQLiteなどのDBに切り替えることができる。
engine = create_engine(
    "postgresql+psycopg2://postgres:root@localhost:5432/graphql_graphene_flask_sqlalchemy_psycopg2_practice",
    echo=True,
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# ベースクラス作成
# 宣言クラスの定義のためにベースクラスを構築する。
# 新しいベースクラスでは、適切なクラスオブジェクトと、クラスとサブクラスを
# 明示的に提供する情報を元にした適切なORMを生成するメタクラスを提供する。
Base = declarative_base()
# セッションのデフォルトで設定済みのクエリクラスのインスタンスを生成
Base.query = db_session.query_property()

# テーブル定義用クラス
class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hired_on = Column(DateTime, default=func.now())
    department_id = Column(Integer, ForeignKey("department.id"))
    department = relationship(
        Department, backref=backref("employees", uselist=True, cascade="delete,all")
    )
