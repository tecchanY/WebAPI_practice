import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Department as DepartmentModel, Employee as EmployeeModel

# RelayはGraphQLの生みの親であるFacebookが作ったReactのためのデータアクセスフレームワーク
# 1.オブジェクトを識別子、確実に同一オブジェクトを再取得できるようにするためのユニークID
# 2.コレクションデータのページネーションに関する情報を表現するための「コネクション」という仕組み
# 3.予測可能なオブジェクトの変更を可能にする仕組み

# REST APIのように必要以上のデータを取得せず、1度で必要な情報を取得できる

# SQLAlchemyObjectTypeを継承したクラスDepartmentとEmployeeでスキーマ定義
# SQLAlchemyObjectTypeとrelay.Connectionを継承したクラスを定義
class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node,)


class DepartmentConnection(relay.Connection):
    class Meta:
        node = Department


class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node,)


class EmployeeGQLConnection(relay.Connection):
    class Meta:
        node = Employee


# 定義したメタクラスによってインスタンス化したものを各変数に格納？
class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_employees = SQLAlchemyConnectionField(EmployeeGQLConnection)
    all_departments = SQLAlchemyConnectionField(DepartmentConnection, sort=None)


# 定義したスキーマであるクラスQueryをSchemaオブジェクトにセット
schema = graphene.Schema(query=Query)
