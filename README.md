#CRUD test application

### Endpoints description

Endpoint  | Method |Parameters | Description
------------- | ------------- | ------------- | -------------
`/books/`  | GET | | Get list of not deleted books
`/books/`| POST | name (string)<br> author(string)<br> rank(int)<br> date_finished(Date)<br> | Create a new book
`/books/<id>` | GET | | Get detail information about book
`/books/<id>` | PUT| rank(int) | Update books rate
`/books/<id>` | DELETE|  | Delete book