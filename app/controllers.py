from flask import Blueprint

#import modules
from app.book.book_controller import book

api = Blueprint('api', __name__, url_prefix='/api')
api.register_blueprint(book)