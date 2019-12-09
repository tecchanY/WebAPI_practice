from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

from sqlalchemy.ext.declarative import declarative_base

# データベースエンジン作成とセッション作成。echo=Trueで発行されるSQL文をログに吐く
# ここの1行を書き換えるだけでMySQLやPostgreSQL、SQLiteなどのDBに切り替えることができる。
# dbの接続条件を変えて複数接続してパーティショニングすることもできる
engine = create_engine(
    "postgresql+psycopg2://postgres:root@localhost:5432/graphql_graphene_flask_sqlalchemy_psycopg2_practice",
    echo=True,
)
# autoflushはデフォルトでtrue
# falseだとsession.commit()しないとadd, update, deleteされない
# rollbackすることで、次のSQLから新規トランザクション開始

# scoped_sessionは同じスレッドで何度Session()コンストラクタを呼び出しても同じSessionインスタンスが返ってくる
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


# database.pyとして分離してもOK
def init_db():
    # メタデータに適切に登録されるように、モデルを定義する可能性のあるすべてのモジュールを
    # ここにインポートします。さもないとinit db（）を呼び出す前に、まずそれらをインポートする必要があります
    from models import Department, Employee

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # オブジェクトを代入した変数をsessionにadd
    # scoped_session() の返すオブジェクトには、Sessionのほとんどのメソッドやプロパティが「クラス」レベルで実装されているので、
    # Session()をインスタンス化する必要はない
    engineering = Department(name="Engineering")
    db_session.add(engineering)
    hr = Department(name="Human Resources")
    db_session.add(hr)

    peter = Employee(name="Peter", department=engineering)
    db_session.add(peter)
    roy = Employee(name="Roy", department=engineering)
    db_session.add(roy)
    tracy = Employee(name="Tracy", department=hr)
    db_session.add(tracy)

    db_session.commit()
