from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app, supports_credentials=True) 
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config["SECRET_KEY"] = "matakewsoblock6"
    db.init_app(app)

    from .routes.auth import auth
    from .routes.notes import note

    app.register_blueprint(auth, url_prefix = "/")
    app.register_blueprint(note, url_prefix = "/")

    from .models import Users, Notes

    return app
