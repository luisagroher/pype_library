import status

from flask import Flask, jsonify
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource
from datetime import datetime, timedelta
from models import UserModel, BookModel, CheckoutsModel
from repo import UserRepo, BookRepo, CheckoutRepo


from faker import Faker

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

class UserList(Resource):
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
    @marshal_with(checkout_fields)
    def get(self):
        return checkout_repo.get_books_due()

class Checkout(Resource):
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
        self.user_is_valid(user_id)
        self.book_is_valid(book_id)
        self.user_limit_reached(user_id)
        self.book_is_out(book_id)

    @marshal_with(checkout_fields)
    def get(self):
        return [c for c in checkout_repo.checkouts.values()]

    @marshal_with(checkout_fields)
    def post(self):
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


def fake_users():
    fake = Faker()
    u = UserModel("a0f18fd8-5044-4182-8d28-905cc28aea2a", "Kimberly Miller", 3)
    user_repo.add_user(u)
    u = UserModel("a34e41e0-8796-4092-b64f-c2d8a5c97bd0", "Melissa Edwards", 3)
    user_repo.add_user(u)
    for i in range(10):
        user_id = fake.uuid4()
        name = fake.name()
        limit=3
        user = UserModel(user_id, name, limit)
        user_repo.add_user(user)
    return jsonify(users=[u.serialize() for u in user_repo.users.values()])

def fake_books():
    fake = Faker()
    b = BookModel("6da03573-5bee-40bc-b43e-84ebe66b0b76", "Emma", "Romance")
    book_repo.add_book(b)
    b = BookModel("5fb5afbd-cf05-4b2c-b369-94dac223279e", "Great Gatsby", "Lit")
    book_repo.add_book(b)
    b = BookModel("2aff469c-6f2f-45cc-ba64-5569e5557015", "Chalk", "Juvenile")
    book_repo.add_book(b)
    b = BookModel("9e79a592-c5bd-4acd-aa16-6a0579a14adc", "The 100", "Sci Fi")
    book_repo.add_book(b)

    for i in range(10):
        book_id = fake.uuid4()
        name = fake.sentence()
        genre =fake.word()
        book = BookModel(book_id, name, genre)
        book_repo.add_book(book)
    return jsonify(books=[b.serialize() for b in book_repo.books.values()])

app = Flask(__name__)
api = Api(app)
api.add_resource(CheckoutList, '/api/checkouts/')
api.add_resource(Checkout, '/api/checkouts/<string:BookId>/<string:UserId>', endpoint='checkout_endpoint')
api.add_resource(UserList, '/api/users/<string:UserId>', endpoint='user_endpoint')
api.add_resource(BookList, '/api/books/due/')
@app.before_first_request
def setup():
    fake_users()
    fake_books()


## Remove these
@app.route('/')
def index():
    return 'Hey, we have Flask in a Docker container!'

@app.route('/users_test/')
def get_user_list():
    return user_repo.list_users()

@app.route('/book_list/')
def get_book_list():
    return book_repo.list_books()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
