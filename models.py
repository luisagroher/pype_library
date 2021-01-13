import os
from datetime import datetime

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, NumberAttribute

dynamodb_host = os.getenv("DYNAMODB_HOST")

def create_tables_if_not_exist():
    if not UserModel.exists():
        UserModel.create_table(read_capacity_units=5, write_capacity_units=2, wait=True)


class UserModel(Model):
    """
    DynamoDB User Table
    """
    class Meta:
        table_name = "users"
        host = dynamodb_host

    UserId = UnicodeAttribute(hash_key=True)
    Name = UnicodeAttribute()
    BookLimit = NumberAttribute(default=10)

    def to_dict(self):
        return self.__dict__['attribute_values']

class BookModel(Model):
    """
    DynamoDB Book Table
    """
    class Meta:
        table_name = 'books'

    BookId = UnicodeAttribute()
    Name = UnicodeAttribute()
    Genre = UnicodeAttribute()

class CheckoutsModel(Model):
    """
    DynamoDB Checkouts Table
    """
    BookId = UnicodeAttribute(hash_key=True)
    UserId = UnicodeAttribute(hash_key=True)
    Date = UTCDateTimeAttribute()
    DueDate = UTCDateTimeAttribute()
