#  import standard library

#  import the third-party library
from werkzeug import generate_password_hash, check_password_hash
from flask import render_template, request, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Email, Length
from flask_login import LoginManager, login_required, logout_user, login_user, current_user

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


class EditUserForm(FlaskForm):
    username = StringField('username', render_kw={'disabled': ''})
    firstname = StringField('firstname', validators=[InputRequired(), Length(min=1, max=50)])
    lastname = StringField('lastname', validators=[InputRequired(), Length(min=1, max=50)])
    bio = TextAreaField('bio', validators=[InputRequired(), Length(min=1, max=500)])

# user_leader (for login manager)
@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))

# index or '/' is the landing page of your website.
# it's the first page that appears when someone navigates into your website.
# make sure your landing page has all the neccesary links for the user to abke to navigate easily
@app.route('/')
def index():
    return render_template('index.html')


#  login for
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for('welcome', username=user.username))
                flash('Invalid Username or Password')
            return render_template('login.html', form=form)
            
# register to 
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
        flash('Successfully registered user')
        return redirect(url_for('index'))

# welcome user after logging in
@app.route('/welcome/me')
@login_required # add login required so that not everyone can access this page!
def welcome():
    username = current_user.username
    return render_template('profile/welcome.html', user=current_user)

# profile of the user
@app.route('/profile/me')
@login_required
def profile():
    return render_template('profile/profile.html', user=current_user) 

# edit te profile of the user
@app.route('/profile/me/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditUserForm()
    if request.method == 'GET':
        form.username.data = current_user.username
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.bio.data = current_user.bio
        return render_template('profile/edit_profile.html', form=form, user=current_user)
    if request.method == 'POST':
        user = User.query.get(current_user.id)
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        flash('Successfully Edited User!')
        return redirect(url_for('profile'))


######### ERROR HANDLING PAGE ##########
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_handler/404.html')

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('You are not logded in')
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('successfully logged out')
    return redirect(url_for('index'))