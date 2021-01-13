from models import UserModel, BookModel, CheckoutsModel
from repo import UserRepo, BookRepo, CheckoutRepo
import status
from flask import current_app, json, url_for
from unittest import TestCase
from api import create_app

class InitialTest(TestCase):
    def setUp(self):
        self.app = create_app()
        self.user_repo = UserRepo()
        self.book_repo = BookRepo()
        self.app_context.push()

    def tearDown(self):
        """ An empty function for removing a database
        """
        pass

    def get_content_type_headers(self):
        return {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        }

    def add_user(self, user_id, name):
        u = UserModel(user_id, name)
        self.user_repo.add_user(user_id, name)

    def add_book(self, book_id, name, checkout_length):
        b = BookModel(book_id, name, checkout_length)
        self.book_repo.add_book(b)

    def add_batch_users(self):
        self.add_user("a0f18fd8-5044-4182-8d28-905cc28aea2a", "Kimberly Miller")
        self.add_user("a34e41e0-8796-4092-b64f-c2d8a5c97bd0", "Melissa Edwards")
        for i in range(10):
            self.add_user(fake.uuid4(), fake.name(), 3)

    def add_batch_books(self):
        self.add_book("6da03573-5bee-40bc-b43e-84ebe66b0b76", "Emma", "Romance")
        self.add_book("5fb5afbd-cf05-4b2c-b369-94dac223279e", "Great Gatsby", "Lit")
        self.add_book("2aff469c-6f2f-45cc-ba64-5569e5557015", "Chalk", "Juvenile")
        self.add_book("9e79a592-c5bd-4acd-aa16-6a0579a14adc", "The 100", "Sci Fi")
        for i in range(10):
            self.add_book(fake.uuid4(), fake.sentence(), fake.word())


    def test_users(self):
        self.add_batch_users()
        self.assertEqual(len(self.user_repo.users), 12)

    def test_books(self):
        self.add_batch_books()
        self.assertEqual(len(self.book_repo.books), 14)

    def test_checkout(self):
        url = url_for()
        data = {"user_id":"luisa groher", "book_id":"d8766917-6cc5-4e10-a18e-85cca4dcf414", "checkout_length":14}
        response = self.test_client.post(
            url, headers=self.get_content_type_headers(),
            data = json.dumps(data)
            )
        return response
