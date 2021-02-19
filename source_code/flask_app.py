import os
from flask import Flask
from source_code.database import init_db

# initialize Flask object reseparetely
def create_app():
    _app = Flask(__name__)
    _app.config.from_object('source_code.config.Config')
    _app.secret_key = os.urandom(24)
    init_db(_app)
    return _app

#  call the create_app() function
app = create_app()