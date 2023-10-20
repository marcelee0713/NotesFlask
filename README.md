# NotesFlask

To Debug

- `python -m venv venv`
- `venv/Scripts/activate`
- CTRL+SHIFT+P
- Select Python Interpreter -> Enter Interpreter Path -> Find -> venv/Scripts/python.exe
- `pip install -r requirements.txt`
- `python server.py`

To Initialize the Database

- type `python`
- `from server import app, db`
- `app.app_context().push()`
- `db.create_all()`
