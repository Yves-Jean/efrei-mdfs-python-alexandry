# Import flask dependencies
from flask import Blueprint, request, flash, g, session, redirect, url_for
# Import the database object from the main app module
from app import db
# Import module models (i.e. User)
from app.book.book_models import Book

book = Blueprint('book', __name__, url_prefix='/book')

# Set the route and accepted methods
@book.route('/', methods=['GET'])
def get():
    return {"books": {
            "isbn":"9781593279509",
            "title":"Eloquent JavaScript, Third Edition",
            "subtitle":"A Modern Introduction to Programming",
            "author":"Marijn Haverbeke",
            "published":"2018-12-04T00:00:00.000Z",
            "publisher":"No Starch Press",
            "pages":472,
            "description":"JavaScript lies at the heart of almost every modern web application, from social apps like Twitter to browser-based game frameworks like Phaser and Babylon. Though simple for beginners to pick up and play with, JavaScript is a flexible, complex language that you can use to build full-scale applications.",
            "website":"http://eloquentjavascript.net/"
        }}