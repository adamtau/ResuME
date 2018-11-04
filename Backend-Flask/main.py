from flask import Flask, render_template, request, redirect, session
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import datetime
#from .User import *
#from .BearFounders import *

app = Flask(__name__)

#####################
# Debug Mode Switch #
#####################

app.config['DEBUG'] = True

#####################
# DB Initialization #
#####################

atlas_username = "admin"
atlas_password = "password1234"
atlas_database = "ResuME"
atlas_uri = "mongodb://" + atlas_username + ":" + atlas_password + "@cluster0-shard-00-00-eqtre.gcp.mongodb.net:27017,cluster0-shard-00-01-eqtre.gcp.mongodb.net:27017,cluster0-shard-00-02-eqtre.gcp.mongodb.net:27017/" + atlas_database + "?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true"
app.config["MONGO_URI"] = atlas_uri
app.config["SECRET_KEY"] = "development key"
mongo = PyMongo(app)
db = mongo.db

#####################
# Web Form Template #
#####################

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    ethnicity = StringField('Ethnicity')
    description = StringField('Description', validators=[DataRequired()])
    address = StringField('Address')
    summary = StringField('Summary')
    bfemail = StringField('BearFounders Email', validators=[DataRequired()])
    bfpassword = PasswordField('BearFounders Password', validators=[DataRequired()])
    submit = SubmitField('Update')

#####################
# Application Route #
#####################

@app.route('/', methods=['GET'])
def hello_world():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # access collections in database
        user_collection = db.users
        # access data in form submission
        email = form.email.data
        username = form.username.data
        password = form.password.data
        # query database if the email is already registered
        user_exist = user_collection.find_one({"email": email})
        # if not, create a new user document in user collection
        if not user_exist:
            new_user = {"email": email,
                        "username": username,
                        "password": password,
                        "date": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}
            user_collection.insert_one(new_user)
        # in both cases, redirect to login page after handling the form
        return redirect('/login')
    else:
        # render register page when form is not submitted yet
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # access collections in database
        user_collection = db.users
        # access data in form submission
        email = form.email.data
        password = form.password.data
        # query database if the email is already registered
        user_exist = user_collection.find_one({"email": email})
        # if not, redirect to register page
        if not user_exist:
            return redirect('/register')
        # else, check if the entered password is correct
        elif password == user_exist["password"]:
            # store the userid locally as an identifying token, redirect to profile page
            session["user_email"] = user_exist["email"]
            return redirect('/profile')
        else:
            # if wrong password is entered, redirect to login page
            return redirect('/login')
    else:
        # render login page when form is not submitted yet
        return render_template('index.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # access collections in database, grab the current profile, ok if empty
    user_collection = db.users
    current_profile = user_collection.find_one({"email": session["user_email"]})
    form = ProfileForm()
    if form.validate_on_submit():
        # access data in form submission
        first_name = form.first_name.data
        last_name = form.last_name.data
        major = form.major.data
        ethnicity = form.ethnicity.data
        description = form.description.data
        address = form.address.data
        summary = form.summary.data
        bfemail = form.bfemail.data
        bfpassword = form.bfpassword.data
        # update the user's profile in profile collection, if not found, create and insert
        user_collection.update(
            {"email": session["user_email"]},
            {'$set': {
                "first_name": first_name,
                "last_name": last_name,
                "major": major,
                "ethnicity": ethnicity,
                "description": description,
                "address": address,
                "summary": summary,
                "bfemail": bfemail,
                "bfpassword": bfpassword
            }}, upsert=False)
        # create a new user object and store locally
        new_user = UserProfile(bfemail, bfpassword, first_name, last_name, major, description)
        bear_modifier = BearFounderModifier(new_user)
        bear_modifier.modify()
        # redirect to profile page, with updated information, ready for next update
        return redirect('/profile')
    else:
        # render profile page when form is not submitted yet
        return render_template('profile.html', form=form)
