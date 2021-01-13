import status

from flask import Flask, jsonify
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource
from datetime import datetime, timedelta
from models import UserModel, BookModel, CheckoutsModel
from repo import UserRepo, BookRepo, CheckoutRepo


from faker import Faker

## the book fields dictionary controls the data that will be rendered in the
## flask_restful response when a book instance is returned
book_fields = {
    'book_url': fields.Url('book_endpoint'),
    'Id': fields.String,
    'Name': fields.String,
    'Genre': fields.String 
    }
## the checkout fields dictionary controls the data that will be rendered
## in the flask_restful response when a checkout instance is returned

checkout_fields = {
    'checkout_uri': fields.Url('checkout_endpoint'),
    'user_url': fields.Url('user_endpoint'),
    'BookId': fields.String,
    'UserId': fields.String,
    'Date': fields.DateTime,
    'DueDate': fields.DateTime
    }


user_repo = UserRepo()
book_repo = BookRepo()
checkout_repo = CheckoutRepo()

## 
class User(Resource):

    """uses the flask__restulf Resource subclass with a get method to return a 
    list of books that a user has checked out when an http method with the same name
    arrives.
    """
    
    def user_exists(self, user_id):
        if user_id not in user_repo.users:
            abort(
                status.HTTP_404_NOT_FOUND,
                message="User with ID {} doesn't exist.".format(user_id))

    @marshal_with(checkout_fields)
    def get(self, UserId):
        self.user_exists(UserId)
        return checkout_repo.get_user_checkout(UserId)


class BookList(Resource):
    @marshal_with(book_fields)
    def get(self):
        return checkout_repo.get_books_due()

class Book(Resource):
    """uses the flask__restful Resource subclass with a get and delete method
    to delete a book using http.
    """

    def book_exists(self, Id):
        if Id not in book_repo.books:
            abort(
                status.HTTP_404_NOT_FOUND,
                message="Book with ID {} doesn't exist.".format(Id))

    @marshal_with(book_fields)
    def get(self, Id):
        return book_repo.get_book(Id)

    def delete(self, Id):
        self.book_exists(Id)
        book_repo.delete_book(Id)
        return '', status.HTTP_204_NO_CONTENT


class Checkout(Resource):
    """
    A checkout resource with methods for the user to get and delete
    a checkout with a http method
    """
    def abort_if_checkout_doesnt_exist(self, book_id, user_id):
        if (book_id, user_id) not in checkout_repo.checkouts:
            abort(
                status.HTTP_404_NOT_FOUND,
                message="Checkout {} doesn't exist.".format(book_id))
   
    @marshal_with(checkout_fields)
    def get(self, BookId, UserId):
        self.abort_if_checkout_doesnt_exist(BookId, UserId)
        return checkout_repo.get_checkout((BookId, UserId))

    def delete(self, book_id, user_id):
        self.abort_if_checkout_doesnt_exist((BookId, UserId))
        checkout_repo.delete_checkout((BookId, UserId))
        return '', status.HTTP_204_NO_CONTENT


class CheckoutList(Resource):
    """
    A checkout resource with methods for the user to get a list of checkouts
    with an http call and a put method for a user to checkout a book with a http call
    """
    def user_is_valid(self, user_id):
        if user_id not in user_repo.users:
            abort(
                status.HTTP_404_NOT_FOUND,
                message="User with ID {} doesn't exist.".format(user_id))
    
    def book_is_valid(self, book_id):
        if book_id not in book_repo.books:
            abort(
                status.HTTP_404_NOT_FOUND,
                message="Book with ID {} doesn't exist.".format(book_id))

    def user_limit_reached(self, user_id):
        user = user_repo.get_user(user_id)
        checkout_number = checkout_repo.get_user_count(user_id)
        if user.BookLimit == checkout_number:
            abort(
                status.HTTP_404_NOT_FOUND,
                message="User with ID {} has reached library limit.".format(user_id))

    def book_is_out(self, book_id):
        if book_id in checkout_repo.get_checkout_books():
            abort(
                status.HTTP_404_NOT_FOUND,
                message="Book with ID {} is checked out.".format(book_id))


    def checkout_is_valid(self, user_id, book_id):
        """checks that the user and book are valid, checks that the user has not reached the library limit,
        checks that the book is available.
        """
        self.user_is_valid(user_id)
        self.book_is_valid(book_id)
        self.user_limit_reached(user_id)
        self.book_is_out(book_id)

    @marshal_with(checkout_fields)
    def get(self):
        """gets a list of checked out books via http
        """
        return [c for c in checkout_repo.checkouts.values()]

    @marshal_with(checkout_fields)
    def post(self):
        """a method to allow a user to checkout a book via http
        """
        parser = reqparse.RequestParser()
        parser.add_argument('book_id')
        parser.add_argument('user_id')
        parser.add_argument('checkout_length')
        args = parser.parse_args()
        ## move to checkout --
        valid = self.checkout_is_valid(
            book_id=args['book_id'],
            user_id=args['user_id'])
        checkout = CheckoutsModel(book_id=args['book_id'],
            user_id=args['user_id'],
            due=int(args['checkout_length']))
        checkout_repo.add_checkout(checkout)
        return checkout, status.HTTP_201_CREATED





## users Faker class to create data
fake = Faker()

def add_fake_user(user_id, name, limit=3):
    """ creates a fake user and adds it to the user repository"""
    u = UserModel(user_id, name, limit)
    user_repo.add_user(u)

def add_fake_book(book_id, name, checkout_length):
    """adds a fake book to the book repository"""
    b = BookModel(book_id, name, checkout_length)
    book_repo.add_book(b)

def add_batch_users():
    """adds a batch of users to the user repository"""
    add_fake_user("a0f18fd8-5044-4182-8d28-905cc28aea2a", "Kimberly Miller")
    add_fake_user("a34e41e0-8796-4092-b64f-c2d8a5c97bd0", "Melissa Edwards", limit=0)
    for i in range(10):
        add_fake_user(fake.uuid4(), fake.name())

def add_batch_books():
    """adds a batch of books to the book factory"""
    add_fake_book("6da03573-5bee-40bc-b43e-84ebe66b0b76", "Emma", "Romance")
    add_fake_book("5fb5afbd-cf05-4b2c-b369-94dac223279e", "Great Gatsby", "Lit")
    add_fake_book("2aff469c-6f2f-45cc-ba64-5569e5557015", "Chalk", "Juvenile")
    add_fake_book("9e79a592-c5bd-4acd-aa16-6a0579a14adc", "The 100", "Sci Fi")
    for i in range(10):
        add_fake_book(fake.uuid4(), fake.sentence(), fake.word())

## A function that initializes the flask application
def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(CheckoutList, '/api/checkouts/')
    api.add_resource(Checkout, '/api/checkouts/<string:BookId>/<string:UserId>', endpoint='checkout_endpoint')
    api.add_resource(User, '/api/users/<string:UserId>', endpoint='user_endpoint')
    api.add_resource(BookList, '/api/books/due/')
    api.add_resource(Book, '/api/books/<string:Id>', endpoint="book_endpoint")
    return app

app = create_app()

@app.before_first_request
def setup():
    """sets up and populates fake data to the user and book repos"""
    add_batch_users()
    add_batch_books()

## Remove these
@app.route('/')
def index():
    """index page 
    """

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
