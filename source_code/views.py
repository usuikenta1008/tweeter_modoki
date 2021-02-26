#  import standard library
import datetime
import json
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


class TweetForm(FlaskForm):
    tweet = TextAreaField('What\'s on your mind', validators=[InputRequired(), Length(min=1, max=300)])

# user_leader (for login manager)
@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))

# index or '/' is the landing page of your website.
# it's the first page that appears when someone navigates into your website.
# make sure your landing page has all the neccesary links for the user to abke to navigate easily
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('newsfeed'))
    else:
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
            
# register to save to the database
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


# Public access profile page
@app.route('/users/<string:username>')
def public_profile(username):
    if current_user.is_authenticated:
        return redirect('view_other_profile', username=username)
    else:
        user = User.quary.filter_by(username=username).first()
        user_id = user.id
        user_bio = user.bio
        return render_template('public_profile.html', username=username, user_bio=user_bio)

# welcome user after logging in
@app.route('/welcome/me')
@login_required # add login required so that not everyone can access this page!
def welcome():
    username = current_user.username
    return render_template('profile/welcome.html', user=current_user)

# profile of the user
# private
@app.route('/profile/me', methods=['GET', 'POST'])
@login_required
def profile(look_tweet_id=None):
    form = TweetForm()
    if request.method == 'GET':
        tweets = PyTweet.query.filter_by(from_user_id=current_user.id).all() #list of tweets
        usernames = []
        for tweet in tweets:
            user = User.query.get(tweet.from_user_id)
            username = user.username
            usernames.append(username)
        tweet_group = list(zip(tweets, usernames))
        tweet_group = tweet_group[::-1]
        return render_template('profile/profile.html', user=current_user, form=form, tweets=tweets, tweet_group=tweet_group, look_tweet_id=look_tweet_id)
    if request.method == 'POST':
        tweet_content = form.tweet.data
        from_user_id = current_user.id
        datetime_now = datetime.datetime.now()
        # convert to format: MM-DD-YYYY hh:mm:ss AM/PM ("02-22-2021 12:22:50 PM")
        datetime_now_string = datetime_now.strftime('%m-%d-%Y %H:%M:%S %p')
        tweet = PyTweet(from_user_id=from_user_id, tweet=tweet_content, datetime_created=datetime_now_string)
        db.session.add(tweet)
        db.session.commit()
        tweet_id = f'tweet-{tweet.tweet_id}'
        return redirect(url_for('profile', look_tweet_id=tweet_id))


# News Feed
@app.route('/newsfeed', methods=['GET', 'POST'])
@login_required
def newsfeed():
    form = TweetForm()
    if request.method == 'GET':
        tweets = PyTweet.query.filter_by(from_user_id=current_user.id).all() #list of tweets
        following_json = current_user.following
        if following_json is not None and following_json != "":
            following = json.loads(following_json)
            for following_id in following:
                tweets = tweets + PyTweet.query.filter_by(from_user_id=following_id).all()

        tweets = sorted(tweets, key=lambda x: x.tweet_id)

        usernames = []
        for tweet in tweets:
            user = User.query.get(tweet.from_user_id)
            username = user.username
            usernames.append(username)
        tweet_group = list(zip(tweets, usernames))
        tweet_group = tweet_group[::-1]
        return render_template('profile/newsfeed.html', user=current_user, form=form, tweet_group=tweet_group)

    if request.method == 'POST':
        tweet_content = form.tweet.data
        from_user_id = current_user.id
        datetime_now = datetime.datetime.now()
        # convert to format: MM-DD-YYYY hh:mm:ss AM/PM ("02-22-2021 12:22:50 PM")
        datetime_now_string = datetime_now.strftime('%m-%d-%Y %H:%M:%S %p')
        tweet = PyTweet(from_user_id=from_user_id, tweet=tweet_content, datetime_created=datetime_now_string)
        db.session.add(tweet)
        db.session.commit()
        tweet_id = f'tweet-{tweet.tweet_id}'
        return redirect(url_for('newsfeed'))


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


@app.route('/profile/me/delete_tweet/<int:tweet_id>')
@login_required
def delete_tweet(tweet_id, to_newsfeed=False):
    tweet = PyTweet.query.get(tweet_id)
    db.session.delete(tweet)
    db.session.commit()
    flash('Successfully Deleted Tweet')
    if to_newsfeed:
        return redirect(url_for('newsfeed'))
    else:
        return redirect(url_for('profile'))

@app.route('/newsfeed/delete/<int:tweet_id>')
@login_required
def delete_tweet_from_newsfeed(tweet_id):
    tweet = PyTweet.query.get(tweet_id)
    db.session.delete(tweet)
    db.session.commit()
    flash('Successfully Deleted Tweet')
    return redirect(url_for('newsfeed'))

# create a page to view others' profile
@app.route('/users/view/<string:username>')
@login_required
def view_other_profile(username):
    user = User.query.filter_by(username=username).first()
    followed = False
    own = False

    tweets = PyTweet.query.filter_by(from_user_id=user.id).all() #list of tweets
    usernames = []
    for tweet in tweets:
        user = User.query.get(tweet.from_user_id)
        username = user.username
        usernames.append(username)
    tweet_group = list(zip(tweets, usernames))
    tweet_group = tweet_group[::-1]
    
    if user.id == current_user.id:
        own = True
    else:
        if user.followers is None or user.followers == "":
            pass
        else:
            followers = json.loads(user.followers)
            if current_user.id in followers:
                followed = True

    return render_template('profile/other_profile.html', user=user, own_profile=own, tweet_group=tweet_group, followed=followed)

# follow this user
@app.route('/follow/<string:username>')
@login_required
def follow_user(username):
    # if you're viewing your own profile, then do nothing
    if username == current_user.username:
        return redirect(url_for('view_other_profile', username=username))
    else:
        user = User.query.get(current_user.id)
        followings_json = user.following
        followed_user = User.query.filter_by(username=username).first()
        followed_user_followers_json = followed_user.followers

        if followings_json is None or followings_json == "":
            following = [followed_user.id]
        else:
            following = json.loads(followings_json)
            if followed_user.id not in following:
                following.append(followed_user.id)
        
        if followed_user_followers_json is None or followed_user_followers_json == "":
            followed_user_followers = [current_user.id]
        else:
            followed_user_followers = json.loads(followed_user_followers_json)
            if current_user.id not in followed_user_followers:
                followed_user_followers.append(current_user.id)

        user.following = json.dumps(following)
        followed_user.followers = json.dumps(followed_user_followers)

        db.session.add(user)
        db.session.add(followed_user)
        db.session.commit()
        flash('Successfully followed User')
        return redirect(url_for('view_other_profile', username=username))

# unfollow this user
@app.route('/unfollow/<string:username>')
@login_required
def unfollow_user(username):
    my_following = json.loads(current_user.following)

    followed_user = User.query.filter_by(username=username).first()
    followed_user_followers = json.loads(followed_user.followers)

    #  remove from my following
    if followed_user.id in my_following:
        my_following.remove(followed_user.id)

    # remove from following user's followers
    if current_user.id in followed_user_followers:
        followed_user_followers.remove(current_user.id)

    user = User.query.get(current_user.id)
    user.following = json.dumps(my_following)
    followed_user.followers = json.dumps(followed_user_followers)

    db.session.add(user)
    db.session.add(followed_user)
    db.session.commit()
    flash('Successfully Unfollowed User!')
    return redirect(url_for('view_other_profile', username=username))

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