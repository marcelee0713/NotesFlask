from flask import Blueprint, jsonify, request, make_response
from ..models import Users
from website import db
auth = Blueprint('auth', __name__)

@auth.route("/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({"message": "Logout successful"}))
    response.set_cookie("userSessionId", value="", expires=0, path="/")
    return response, 200

@auth.route("/login", methods=["POST"])
def login():
    req = request.get_json()
    username = req.get("username")
    password = req.get("password")

    # Find the user by their username
    user = Users.query.filter_by(username=username).first()

    # Check if the user exists and if the password is correct
    if user and user.password == password:
        response = jsonify({"username": str(user.username), "id": str(user.id)})
        return response, 200
    else:
        return make_response(jsonify({"message": "Invalid username or password"}), 401)

@auth.route("/sign-up", methods=["POST"])
def signUp():
    req = request.get_json()
    username = req.get("username")
    password = req.get("password")

    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        return make_response(jsonify({"message": "Username already exists"}), 409)

    new_user = Users(username=username, password=password)

    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify({"message": "Signup successful"}), 200) 