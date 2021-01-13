from marshmallow import Schema, fields, pre_load
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()

class AddUpdateDelete():
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()

class UserModel(db.Model, AddUpdateDelete):
    """a class to represent users with a constructor that initializes 
    the user id, name, and limit attributes. The default checkout limit is 3"""
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    limit = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, name, limit=3):
        self.Id = user_id
        self.Name = name
        self.BookLimit = limit

    def serialize(self):
        return {
        'Id': self.Id,
        'Name': self.Name,
        'BookLimit': self.BookLimit
        }


class BookModel(db.Model, AddUpdateDelete):
    """a class to represent books with a constructor that initializes
    the book id, book name, and genre attributes"""
    bid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    genre = db.Column(db.String(250), nullable=False)
    
    def __init__(self, book_id, name, genre):
        self.Id = book_id
        self.Name = name
        self.Genre = genre

    def serialize(self):
        return {
        'Id': self.Id,
        'Name': self.Name,
        'Genre': self.Genre
        }

class CheckoutsModel(db.Model, AddUpdateDelete):
    """a class to represent checkout with a constructor that initializes the
    book id, book name, checkout date and due date attributes"""
    cid = db.Column(db.Integer, primary_key=True)
    book_id =  db.relationship('BookModel')
    user_id = db.relationship('UserModel')
    checkout_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    due_date = db.Column(db.TIMESTAMP, nullable=False)
    
    def __init__(self, user_id, book_id, checkout_date=datetime.today(), due=14):
        self.BookId = book_id
        self.UserId = user_id
        self.Date = checkout_date
        self.DueDate = self.Date + timedelta(days=due)