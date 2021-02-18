from flask import Flask

# initialize Flask object reseparetely
def create_app():
    _app = Flask(__name__)

    return _app

#  call the create_app() function
app = create_app()