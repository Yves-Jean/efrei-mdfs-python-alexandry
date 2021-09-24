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
def hello_world():
    return "<h1>Welcome to the Alexandry API</h1>"

# Import a module / component using its blueprint handler variable (mod_auth)
# from app.book.book_controller import Book_controller as book_module

