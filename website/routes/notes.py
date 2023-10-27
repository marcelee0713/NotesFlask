from flask import Blueprint, jsonify, request, make_response
from ..models import Notes
from website import db
note = Blueprint('notes', __name__)


@note.route("/create-note", methods=["POST"])
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

@note.route("/get-user-notes", methods=["GET"])
def get_user_notes():
    userId = request.args.get("userId")

    if not userId:
        return make_response(jsonify({"message": "User id is missing!"}), 404)

    user_notes = Notes.query.filter_by(user_id=userId).all()

    user_notes_list = [note.as_dict() for note in user_notes]

    return make_response(jsonify(user_notes_list), 200)
    
@note.route("/update-note", methods=["PUT"])
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

@note.route("/delete-note", methods=["DELETE"])
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