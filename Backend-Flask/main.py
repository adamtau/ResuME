from flask import Flask, render_template, request, redirect, session
from flask_pymongo import PyMongo
import datetime
from .User import *
from .BearFounders import *

app = Flask(__name__)

#####################
# Debug mode switch #
#####################

app.config['DEBUG'] = True
atlas_username = "admin"
atlas_password = "password1234"
atlas_database = "ResuME"
atlas_uri = "mongodb://" + atlas_username + ":" + atlas_password + "@cluster0-shard-00-00-eqtre.gcp.mongodb.net:27017,cluster0-shard-00-01-eqtre.gcp.mongodb.net:27017,cluster0-shard-00-02-eqtre.gcp.mongodb.net:27017/" + atlas_database + "?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true"

#####################
# DB Initialization #
#####################

app.config["MONGO_URI"] = atlas_uri
app.config["SECRET_KEY"] = "development key"
mongo = PyMongo(app)
db = mongo.db

#####################
# Application Route #
#####################

@app.route('/', methods=['GET'])
def hello_world():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.form and request.method == "POST":
        # access collections in database
        user_collection = db.users
        # access data in form submission
        action = request.form.get('action')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
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
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.form and request.method == "POST":
        # access collections in database
        user_collection = db.users
        # access data in form submission
        action = request.form.get('action')
        email = request.form.get('email')
        password = request.form.get('password')
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
        return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.form and request.method == "POST":
        # access collections in database, grab the current profile, ok if empty
        user_collection = db.users
        current_profile = user_collection.find_one({"email": session["user_email"]})
        # access data in form submission
        action = request.form.get('action')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        major = request.form.get('major')
        description = request.form.get('description')
        bfemail = request.form.get('bfemail')
        bfpassword = request.form.get('bfpassword')
        # update the user's profile in profile collection, if not found, create and insert 
        user_collection.update(
            {"email": session["user_email"]},
            {'$set': {
                "first_name": first_name,
                "last_name": last_name,
                "major": major,
                "description": description,
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
        return render_template('profile.html')
