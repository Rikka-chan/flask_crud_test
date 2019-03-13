from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .models import Book

    def jsonify_book(book):
        return jsonify({
                    'id': book.id,
                    'name': book.name,
                    'date_finished': book.date_finished,
                    'author': book.author,
                    'rank': book.rank
                })

    @app.route('/books/', methods=['POST', 'GET'])
    def books():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            if name:
                book = Book(**request.data)
                book.save()
                response = jsonify_book(book)
                response.status_code = 201
                return response
        else:
            # GET
            books = Book.get_all()
            results = []

            for book in books:
                obj = {
                    'id': book.id,
                    'name': book.name,
                    'date_finished': book.date_finished,
                    'author': book.author,
                    'rank': book.rank
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def books_manipulation(id, **kwargs):
        # retrieve a book using it's ID
        book = Book.query.filter_by(id=id, deleted=False).first()
        if not book:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            book.delete()
            return {
                       "message": "book {} deleted successfully".format(book.id)
                   }, 200

        elif request.method == 'PUT':
            if 'rank' not in request.data:
                response = jsonify({
                    'no_field': 'rank field is required'
                })
                response.status_code = 400
                return response

            rank = str(request.data.get('rank', ''))
            book.rank = rank
            book.save()
            response = jsonify_book(book)
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify_book(book)
            response.status_code = 200
            return response

    return app
