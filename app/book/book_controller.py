# Import flask dependencies
from app.book.book_models import Book
from flask import Blueprint, request, flash, g, session, redirect, url_for,abort,render_template
import os,sys,json
# Import the database object from the main app module
from app.db import Database
from app.clients import SQLiteClient,JsonClient

parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../storage/database.sqlite"))
client = SQLiteClient(parentddir)
db = Database(client).get_client()



book = Blueprint('book', __name__, url_prefix='/book')

def check_if_exist(book_id):
    book = db.findOne(book_id)
    print(book)
    if not book:
        abort(404,"This book does not exist")
    return book

@book.route('/', methods=['GET'])
def get_all():
    data = db.find()
    data = json.dumps(data)
    return data,200

@book.route('/<book_id>', methods=['GET'])
def get_one_by_id(book_id):
    book = check_if_exist(book_id)
    book = json.dumps(book)
    return book,200

    
@book.route('/add',methods=['POST'])
def create():
    new_book = db.create(request.get_json())
    print(new_book)
    return json.dumps(new_book),200

@book.route('/',methods=['PUT'])
def edit_by_id():
    book = check_if_exist(request.get_json()['isbn'])
    book["title"]=request.get_json()['title']
    book["subtitle"]=request.get_json()['subtitle']
    book["author"]=request.get_json()['author']
    book["published"]=request.get_json()['published']
    book["publisher"]=request.get_json()['publisher']
    book["pages"]=request.get_json()['pages']
    book["description"]=request.get_json()['description']
    book["website"]=request.get_json()['website']
    db.update(book)
    return json.dumps(book),200

@book.route('/<book_id>',methods=['DELETE'])
def delete_by_id(book_id):
    deleted = db.delete(book_id)
    if deleted :
        return "Book %s has been deleted successfully."  % (book_id),204
    else :
        return {"status": None, "message":"Nothing has been deleted"}