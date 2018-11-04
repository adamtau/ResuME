from flask import Flask, render_template, request, redirect, session
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FormField, TextAreaField, DateField
from wtforms.validators import DataRequired, ValidationError
from datetime import date, time, datetime
from User import *
from BearFounders import *

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
app.config["WTF_CSRF_CHECK_DEFAULT"] = False
mongo = PyMongo(app)
db = mongo.db

#####################
# Web Form Template #
#####################

class RegisterForm(FlaskForm):
    email = StringField('Email', render_kw={'placeholder': 'example@example.com'}, validators=[DataRequired()])
    password = PasswordField('Password', render_kw={'placeholder': 'password'}, validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', render_kw={'placeholder': 'example@example.com'}, validators=[DataRequired()])
    password = PasswordField('Password', render_kw={'placeholder': 'password'}, validators=[DataRequired()])
    submit = SubmitField('Log In')

class EducationEntryForm(FlaskForm):
    school = StringField('School', render_kw={'placeholder': 'school name'})
    major = StringField('Major', render_kw={'placeholder': 'major'})
    start_date = StringField("Start Date", render_kw={'placeholder': '06/21/2018 for June 21, 2018'})
    end_date = StringField("End Date", render_kw={'placeholder': '06/21/2018 for June 21, 2018'})
    location = StringField('Location', render_kw={'placeholder': 'school location'})

class ExperienceEntryForm(FlaskForm):
    title = StringField('Title')
    start_date = StringField("Start Date", render_kw={'placeholder': '06/21/2018 for June 21, 2018'})
    end_date = StringField("End Date", render_kw={'placeholder': '06/21/2018 for June 21, 2018'})
    company = StringField('Company', render_kw={'placeholder': 'company name'})
    location = StringField('Location', render_kw={'placeholder': 'company location'})
    exp_description = TextAreaField('Description', render_kw={'placeholder': 'experience description'})

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', render_kw={'placeholder': 'first name'}, validators=[DataRequired()])
    last_name = StringField('Last Name', render_kw={'placeholder': 'last name'}, validators=[DataRequired()])
    major = StringField('Major', render_kw={'placeholder': 'your major'}, validators=[DataRequired()])
    ethnicity = StringField('Ethnicity', render_kw={'placeholder': 'your ethnicity, optional'})
    description = TextAreaField('Description', render_kw={'placeholder': 'describe yourself'}, validators=[DataRequired()])
    address = StringField('Address', render_kw={'placeholder': 'your current address'})
    summary = TextAreaField('Summary', render_kw={'placeholder': 'summarize your profile'})
    bfemail = StringField('BearFounders Email', render_kw={'placeholder': 'BearFounders email'}, validators=[DataRequired()])
    bfpassword = PasswordField('BearFounders Password', render_kw={'placeholder': 'BearFounders password'}, validators=[DataRequired()])
    educations = FieldList(FormField(EducationEntryForm))
    experiences = FieldList(FormField(ExperienceEntryForm))
    submit = SubmitField('Update')

#####################
# Application Route #
#####################

@app.route('/', methods=['GET'])
def hello_world():
    session["user_email"] = ""
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.is_submitted():
        # access collections in database
        user_collection = db.users
        # access data in form submission
        email = form.email.data
        password = form.password.data
        # query database if the email is already registered
        user_exist = user_collection.find_one({"email": email})
        # if not, create a new user document in user collection
        if not user_exist:
            new_user = {"email": email, 
                        "password": password, 
                        "date": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}
            user_collection.insert_one(new_user)
        # in both cases, redirect to login page after handling the form
        session["user_email"] = email
        return redirect('/login')
    else:
        # render register page when form is not submitted yet
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(email=session["user_email"])
    if form.is_submitted():
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
        return render_template('login.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # access collections in database, grab the current profile, ok if empty
    user_collection = db.users
    current_profile = user_collection.find_one({"email": session["user_email"]})
    # create a profile_form instance, populated by profile data
    form = ProfileForm(data=current_profile)
    form.educations.append_entry()
    form.experiences.append_entry()
    # loop through profile experiences, create instances of experience_entry_form, append to profile_form
    if form.is_submitted():
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
        # loop through submitted form entries to collect current experiences/educations
        current_educations = []
        for edu in form.educations.entries:
            edu_data = {"school": edu.data["school"], 
                        "major": edu.data["major"], 
                        "location": edu.data["location"], 
                        "start_date": edu.data["start_date"],
                        "end_date": edu.data["end_date"]}
                        # "start_date": datetime.combine(edu.data["start_date"], time(12, 30)),
                        # "end_date": datetime.combine(edu.data["end_date"], time(12, 30))}
            if edu_data["school"]:
            	current_educations.append(edu_data)
        current_experiences = []
        for exp in form.experiences.entries:
            exp_data = {"title": exp.data["title"], 
                        "company": exp.data["company"], 
                        "location": exp.data["location"], 
                        "exp_description": exp.data["exp_description"],
                        "start_date": exp.data["start_date"],
                        "end_date": exp.data["end_date"]}
                        # "start_date": datetime.combine(exp.data["start_date"], time(12, 30)),
                        # "end_date": datetime.combine(exp.data["end_date"], time(12, 30))}
            if exp_data["title"]:
            	current_experiences.append(exp_data)
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
                "bfpassword": bfpassword,
                "educations": current_educations,
                "experiences": current_experiences 
            }}, upsert=True)
        # create a new user object and store locally
        # new_user = UserProfile(bfemail, bfpassword, first_name, last_name, major, description)
        # bear_modifier = BearFounderModifier(new_user)
        # bear_modifier.modify()
        # redirect to profile page, with updated information, ready for next update
        return redirect('/profile')
    else:
        # render profile page when form is not submitted yet
        return render_template('profile.html', form=form)

