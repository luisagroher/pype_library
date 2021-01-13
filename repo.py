from datetime import datetime, timedelta
from flask import jsonify
# from models import UserModel, BookModel, CheckoutsModel

class UserRepo():
    """
    persists the UserModel intances into an in-memory dictionary
    with methods to retrieve, insert, update, and delete new users
    """
    def __init__(self):
        self.users = {}
    
    def add_user(self, user):
        self.users[user.Id] = user

    def get_user_by_name(self, username):
        """an o(n) operation can do it in o(1)"""
        return [u for u in self.users.values() if u.Name == username]
    
    def get_user(self, user_id):
        return self.users[user_id]

    def delete_user(self, id):
        del self.users[id]
    
    def list_users(self):
        return jsonify(users=[u.serialize() for u in self.users.values()])

class BookRepo():
    """
    persists the BookModel instances into an in-memory dictionary
    with methods to retrieve, insert, update and delete books
    """
    def __init__(self):
        self.books = {}

    def add_book(self, book):
        self.books[book.Id] = book

    def get_book(self, book_id):
        return self.books[book_id]

    def get_book_name(self, bookname):
        for key in self.users:
            if self.users[key].Name == bookname:
                return key
    
    def get_book_names(self):
        return [b.Name for b in self.books]
    
    def delete_book(self, id):
        del self.books[id]
    
    def list_books(self):
        return jsonify(books=[b.serialize() for b in self.books.values()])

class CheckoutRepo():
    """
    Persists the CheckoutModel instances into an in memory dictionary
    with methods to retrieve, insert, update and delete checkouts
    """
    def __init__(self):
        #self.checkout_history = {}
        self.checkouts = {}

    def add_checkout(self, checkout):
        self.checkouts[(checkout.BookId, checkout.UserId)] = checkout  
    
    def get_checkout(self, book_id, user_id):
        return self.checkouts[(book_id, user_id)]
    
    def get_checkout_books(self):
        return [c[0] for c in self.checkouts.keys() if self.checkouts[c].DueDate >= datetime.today()]
    
    def get_checkout_users(self):
        return [c[1] for c in self.checkouts.keys()]

    def get_user_checkout(self, user_id):
        return [c for c in self.checkouts.values() if c.UserId == user_id]
    
    def get_users_count(self):
        from collections import Counter
        user_ids = self.get_checkout_users()
        return dict(Counter(user_ids))
    
    def get_user_count(self, user_id):
        if user_id in self.get_users_count():
            return self.get_users_count()[user_id]
        else:
            return 0

    def get_books_due(self):
        return [c for c in self.checkouts.values() if c.DueDate < datetime.today() + timedelta(days=3) ]

