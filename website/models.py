from website import db
from datetime import datetime

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