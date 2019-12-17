from database.base import db_session
from flask import Flask
from flask_graphql import GraphQLView
from schema import schema

# from setup import init_db

app = Flask(__name__)
app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    # init_db()
    app.run(threaded=True, debug=True)
