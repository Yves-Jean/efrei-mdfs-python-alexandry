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
    return "<h1>Welcome to the Alexandry API</h1>"

# modules
from app.controllers import api

# Register blueprint(s)
app.register_blueprint(api)

