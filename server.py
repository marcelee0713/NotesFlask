from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

# app instance
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, supports_credentials=True) 

# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
# Secret Key
app.config["SECRET_KEY"] = "matakewsoblock6"
# Init db
db = SQLAlchemy()
db.init_app(app)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    date_added = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    notes = db.relationship('Notes')

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

@app.route("/api/home", methods=["GET"])
def return_home():
    return jsonify({
        'message': "Hello world"
    })

@app.route("/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({"message": "Logout successful"}))
    response.set_cookie("userSessionId", value="", expires=0, path="/")
    return response, 200

@app.route("/login", methods=["POST"])
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

@app.route("/sign-up", methods=["POST"])
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
    
@app.route("/create-note", methods=["POST"])
def createNote():
    req = request.get_json()
    note = req.get("note")
    userId = req.get("userId")

    if(userId == "" ):
        return make_response(jsonify({"message": "User id is missing!"}), 404)
    
    if(note == ""):
        return make_response(jsonify({"message": "No note provided!"}), 404)
    
    new_note = Notes(data=note, user_id=userId)
    db.session.add(new_note)
    db.session.commit()

    return make_response(jsonify(new_note.as_dict()), 200) 

@app.route("/get-user-notes", methods=["GET"])
def get_user_notes():
    userId = request.args.get("userId")

    if not userId:
        return make_response(jsonify({"message": "User id is missing!"}), 404)

    user_notes = Notes.query.filter_by(user_id=userId).all()

    user_notes_list = [note.as_dict() for note in user_notes]

    return make_response(jsonify(user_notes_list), 200)
    
@app.route("/update-note", methods=["PUT"])
def update_note():
    note_id = request.json.get("noteId") 
    new_data = request.json.get("newNote")
    user_id = request.json.get("userId")  

    if not note_id:
        return make_response(jsonify({"message": "Note ID is missing!"}), 404)

    if new_data is None:
        return make_response(jsonify({"message": "New data is missing!"}), 400)

    if not user_id:
        return make_response(jsonify({"message": "User ID is missing!"}), 404)

    note_to_update = Notes.query.get(note_id)

    if note_to_update is None:
        return make_response(jsonify({"message": "Note not found!"}), 404)
    
    if str(note_to_update.user_id) != user_id:
        return make_response(jsonify({"message": "Unauthorized to update this note!"}), 403)

    note_to_update.data = new_data

    db.session.commit()

    return make_response(jsonify({"message": "Note updated successfully"}), 200)

@app.route("/delete-note", methods=["DELETE"])
def delete_note():
    note_id = request.json.get("noteId")  
    user_id = request.json.get("userId")  

    if not note_id:
        return make_response(jsonify({"message": "Note ID is missing!"}), 404)

    if not user_id:
        return make_response(jsonify({"message": "User ID is missing!"}), 404)

    note_to_delete = Notes.query.get(note_id)

    if note_to_delete is None:
        return make_response(jsonify({"message": "Note not found!"}), 404)

    if str(note_to_delete.user_id) != user_id:
        return make_response(jsonify({"message": "Unauthorized to delete this note!"}), 403)

    db.session.delete(note_to_delete)
    db.session.commit()

    return make_response(jsonify({"message": "Note deleted successfully"}), 200)


if __name__ == "__main__":
    app.run(debug=True)
    

with app.app_context():
    db.create_all()