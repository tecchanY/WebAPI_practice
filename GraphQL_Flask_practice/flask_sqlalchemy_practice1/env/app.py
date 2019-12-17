from flask import Flask
from flask_graphql import GraphQLView

from models import db_session
from schema import schema

# 今回のファイル構成ではコマンドラインから直接このファイルが呼ばれるのではなく、
# import文で他のプログラムから参照されるため、__name__には参照元のファイル名が格納される。

# フォーカスすると表示される説明によると、from flask import Flask　app = Flask(__name__)というのは
# メインモジュールか__init__.pyに記述する。Flaskインスタンスを作成する。
app = Flask(__name__)
app.debug = True

example_query = """
{
    allEmployees{
        edges{
            node{
                id
                name
                department{
                    id
                    name
                }
            }
        }
    }
}
"""

# apiと対話するための唯一のエンドポイント（URL）を指定
app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("/graphql", schema=schema, graphiql=True)
)

# フォーカスすると表示される説明によると、@app.teardown_appcontextはアプリケーション終了時の処理を書くときに必要なアノテーションっぽい。
@app.teardown_appcontext
def shutdown_session(exception):
    if exception and db_session.is_active:
        db_session.rollback
    else:
        # db_session.commit()
        pass
    db_session.close()


# おまじない
if __name__ == "__main__":
    # init_db()
    app.run()
