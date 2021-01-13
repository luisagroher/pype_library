An RESTful API for library management application.  It uses an in-memory dictionary 
to manage users, books, and library checkouts.  The management functions simulate a database but
should be swapped out for a database.  

The API gets information from calls to the app to:
- report how many books a user has checked out
- report a list of books that are near the deadline
- allow a book to be checked out to a user

Dependencies:
- flask
- flask-restful

## Installation
# Docker
```
```

# Curl Methods

User does not exist
```
curl -iX POST -H "Content-Type: application/json" -d '{"user_id":"luisa groher", "book_id":"d8766917-6cc5-4e10-a18e-85cca4dcf414", "checkout_length":14}' http://0.0.0.0:5000//api/checkouts/
```

Book does not exist
```
curl -iX POST -H "Content-Type: application/json" -d '{"user_id":"a34e41e0-8796-4092-b64f-c2d8a5c97bd0", "book_id":"greatgatsby", "checkout_length":14}' http://0.0.0.0:5000//api/checkouts/
```

User reached limit
```
curl -iX POST -H "Content-Type: application/json" -d '{"user_id":"a0f18fd8-5044-4182-8d28-905cc28aea2a", "book_id":"6da03573-5bee-40bc-b43e-84ebe66b0b76", "checkout_length":14}' http://0.0.0.0:5000//api/checkouts/
```

```
curl -iX POST -H "Content-Type: application/json" -d '{"user_id":"a0f18fd8-5044-4182-8d28-905cc28aea2a", "book_id":"5fb5afbd-cf05-4b2c-b369-94dac223279e", "checkout_length":14}' http://0.0.0.0:5000//api/checkouts/
```

```
curl -iX POST -H "Content-Type: application/json" -d '{"user_id":"a0f18fd8-5044-4182-8d28-905cc28aea2a", "book_id":"2aff469c-6f2f-45cc-ba64-5569e5557015", "checkout_length":1}' http://0.0.0.0:5000//api/checkouts/
```

```
curl -iX POST -H "Content-Type: application/json" -d '{"user_id":"a0f18fd8-5044-4182-8d28-905cc28aea2a", "book_id":"9e79a592-c5bd-4acd-aa16-6a0579a14adc", "checkout_length":14}' http://0.0.0.0:5000//api/checkouts/
```

Book is checked out

```
curl -iX POST -H "Content-Type: application/json" -d '{"user_id":"a34e41e0-8796-4092-b64f-c2d8a5c97bd0", "book_id":"6da03573-5bee-40bc-b43e-84ebe66b0b76", "checkout_length":14}' http://0.0.0.0:5000/api/checkouts/
```


Delete a book
```
curl -iX DELETE http://0.0.0.0:5000/api/books/9e79a592-c5bd-4acd-aa16-6a0579a14adc
```

```
curl -iX POST -H "Content-Type: application/json" -d '{"user_id":"a34e41e0-8796-4092-b64f-c2d8a5c97bd0", "book_id":"9e79a592-c5bd-4acd-aa16-6a0579a14adc", "checkout_length":14}' http://0.0.0.0:5000//api/checkouts/
```