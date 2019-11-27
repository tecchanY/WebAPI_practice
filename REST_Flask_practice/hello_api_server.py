from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

members = ["John", "Bill", "Eric"]
# 実際のAPIではデータベースからリソースのデータを取得する場合も多い


@app.route("/")
def get_hello():
    return jsonify({"message": "Hello from Flask API Server!"})


@app.route("/members")
def get_all_members():
    return jsonify({"members": members})


@app.route("/members/<int:index>")
def get_member(index):
    return jsonify({"member": members[index]})


@app.route("/members", methods=["POST"])
def add_member():
    posted = request.get_json()
    members.append(posted["member"])
    return jsonify({"message": "new member added"})


@app.route("/members/<int:index>", methods=["PUT"])
def update_member(index):
    posted = request.get_json()
    members[index] = posted["member"]
    return jsonify({"message": "member updated"})


@app.route("/members/<int:index>", methods=["DELETE"])
def delete_member(index):
    members.pop(index)
    return jsonify({"message": "member deleted"})


if __name__ == "__main__":
    app.run(debug=True)
