import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .models import db_session, ModelDepartment, ModelEmployee

# RelayはGraphQLの生みの親であるFacebookが作ったReactのためのデータアクセスフレームワーク
# 1.オブジェクトを識別子、確実に同一オブジェクトを再取得できるようにするためのユニークID
# 2.コレクションデータのページネーションに関する情報を表現するための「コネクション」という仕組み
# 3.予測可能なオブジェクトの変更を可能にする仕組み

# REST APIのように必要以上のデータを取得せず、1度で必要な情報を取得できる

# SQLAlchemyObjectTypeを継承したクラスDepartmentとEmployeeでスキーマ定義
# SQLAlchemyObjectTypeとrelay.Connectionを継承したクラスを定義

# クラスにはフィールドとフィールドのリゾルバ関数を実装


class DepartmentAttribute:
    name = graphene.String()


class EmployeeAttribute:
    name = graphene.String()
    hired_on = graphene.DateTime()
    department_id = graphene.ID()


class DepartmentNode(SQLAlchemyObjectType, DepartmentAttribute):
    class Meta:
        model = ModelDepartment
        interfaces = (relay.Node,)


# class DepartmentGQLConnection(relay.Connection):
#     class Meta:
#         node = Department


class CreateDepartmentInput(graphene.InputObjectType, DepartmentAttribute):
    """Arguments to create a department"""
    class Meta:
        node = DepartmentNode


class UpdateDepartmentInput(graphene.InputObjectType, DepartmentAttribute):
    """Arguments to create a department"""
    id = graphene.ID(required=True)

    class Meta:
        node = DepartmentNode


class EmployeeNode(SQLAlchemyObjectType, EmployeeAttribute):
    class Meta:
        model = ModelEmployee
        interfaces = (relay.Node,)


# class EmployeeGQLConnection(relay.Connection):
#     class Meta:
#         node = Employee


class CreateEmployeeInput(graphene.InputObjectType, EmployeeAttribute):
    """Arguments to create a employee"""
    class Meta:
        node = EmployeeNode


class UpdateEmployeeInput(graphene.InputObjectType, EmployeeAttribute):
    """Arguments to create a employee"""
    id = graphene.ID(required=True)

    class Meta:
        node = EmployeeNode


class CreateDepartment(graphene.Mutation):
    # id, nameが戻り値(レスポンス)
    # Inputを書いてるのと同じ
    # id = graphene.ID()
    # name = graphene.String()

    department = graphene.Field(lambda: ModelDepartment)

    class Arguments:
        input = CreateDepartmentInput(required=True)
        # nameがString型のフィールドで、サーバーに送信するクエリにおけるDepartmentの引数
        # id = graphene.ID()
        # name = graphene.String()

    # nameフィールドのリゾルバ関数
    # mutateメソッドの引数はself, infoの次に引数が並ぶ

    def mutate(self, info, input):
        department = ModelDepartment(input)
        # ここで永続化
        # ↑これはsqlite3でインメモリに保存してる場合の話？

        db_session.add(department)
        db_session.commit()

        # Mutationを継承したクラスをインスタンス化して返す
        return CreateDepartment(department=department)
        # return CreateDepartment(department=department)


class UpdateDepartment(graphene.Mutation):
    department = graphene.Field(lambda: ModelDepartment)

    class Arguments:
        input = UpdateDepartmentInput(required=True)

    def mutate(self, info, input):
        department = ModelDepartment(input)

        db_session.add(department)
        db_session.commit()

        return UpdateDepartment(department=department)


class CreateEmployee(graphene.Mutation):
    employee = graphene.Field(lambda: ModelEmployee)

    class Arguments:
        input = CreateEmployeeInput(required=True)

    def mutate(self, info, input):
        employee = ModelEmployee(input)

        db_session.add(employee)
        db_session.commit()

        return CreateEmployee(employee=employee)


class UpdateEmployee(graphene.Mutation):
    employee = graphene.Field(lambda: ModelEmployee)

    class Arguments:
        input = UpdateEmployeeInput(required=True)

    def mutate(self, info, input):
        employee = ModelEmployee(input)

        db_session.add(employee)
        db_session.commit()

        return UpdateEmployee(employee=employee)

# 定義したメタクラスによってインスタンス化したものを各変数に格納？


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    employee = relay.Node.Field(ModelEmployee)
    department = relay.Node.Field(ModelDepartment)

    employeeList = SQLAlchemyConnectionField(ModelEmployee)
    departmentList = SQLAlchemyConnectionField(ModelDepartment)


class MyMutation(graphene.ObjectType):
    create_department = CreateDepartment.Field()
    update_department = UpdateDepartment.Field()
    create_employee = CreateEmployee.Field()
    update_employee = UpdateEmployee.Field()


# 定義したスキーマであるクラスQueryをSchemaオブジェクトにセット
schema = graphene.Schema(query=Query, mutation=MyMutation)
