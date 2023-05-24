from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random

db = SQLAlchemy()
# short_url = db.Column(db.String(3), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    bookmarks = db.relationship("Bookmark", backref="user", passive_deletes=True)


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3), nullable=False)
    visits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    def generate_unique_characters(self):
        characters = string.digits+string.ascii_letters
        picked_char = random.choices(characters, k=3)
        joined_char = "".join(picked_char)

        link = self.query.filter_by(short_url=joined_char).first()
        if link:
            self.generate_unique_characters()
        else:
            return joined_char

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_unique_characters()