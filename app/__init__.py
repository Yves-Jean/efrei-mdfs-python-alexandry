# Import flask and template operators
from flask import Flask, render_template

# Define the WSGI application object
app = Flask(__name__)


# Configurations
app.config.from_object('config')

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404/404.html'), 404

@app.route("/")
def welcome():
    return render_template('home/home.html')

@app.route("/book/<book_id>")
def display_book(book_id):
    return render_template('book/book.html')

# modules
from app.controllers import api

# Register blueprint(s)
app.register_blueprint(api)

