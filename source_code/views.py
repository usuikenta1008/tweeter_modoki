#  import standard library

#  import the third-party library
from werkzeug import generate_password_hash, check_password_hash
from flask import render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, login_required, logout_user

# import your own modules/packages
from source_code import app, db
from source_code.models import *

bootstrap = Bootstrap(app)

login_manager =LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remenber me')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

# index or '/' is the landing page of your website.
# it's the first page that appears when someone navigates into your website.
# make sure your landing page has all the neccesary links for the user to abke to navigate easily
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    if request.method == 'POST':
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))


######### ERROR HANDLING PAGE ##########
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_handler/404.html')