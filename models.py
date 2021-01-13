import hashlib
from datetime import datetime, timedelta

class UserModel:
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


class BookModel:
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

class CheckoutsModel:
    def __init__(self, user_id, book_id, checkout_date=datetime.today(), due=14):
        self.BookId = book_id
        self.UserId = user_id
        self.Date = checkout_date
        self.DueDate = self.Date + timedelta(days=due)