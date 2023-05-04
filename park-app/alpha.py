from hashlib import md5
from typing import Optional

import requests
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import (
    BooleanField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

# __init__.py
# app_list.py
STATE_LIST = [
    ("AL", "Alabama"),
    ("AK", "Alaska"),
    ("AZ", "Arizona"),
    ("AR", "Arkansas"),
    ("CA", "California"),
    ("CO", "Colorado"),
    ("CT", "Connecticut"),
    ("DE", "Delaware"),
    ("FL", "Florida"),
    ("GA", "Georgia"),
    ("HI", "Hawaii"),
    ("ID", "Idaho"),
    ("IL", "Illinois"),
    ("IN", "Indiana"),
    ("IA", "Iowa"),
    ("KS", "Kansas"),
    ("KY", "Kentucky"),
    ("LA", "Louisiana"),
    ("ME", "Maine"),
    ("MD", "Maryland"),
    ("MA", "Massachusetts"),
    ("MI", "Michigan"),
    ("MN", "Minnesota"),
    ("MS", "Mississippi"),
    ("MO", "Missouri"),
    ("MT", "Montana"),
    ("NE", "Nebraska"),
    ("NV", "Nevada"),
    ("NH", "New Hampshire"),
    ("NJ", "New Jersey"),
    ("NM", "New Mexico"),
    ("NY", "New York"),
    ("NC", "North Carolina"),
    ("ND", "North Dakota"),
    ("OH", "Ohio"),
    ("OK", "Oklahoma"),
    ("OR", "Oregon"),
    ("PA", "Pennsylvania"),
    ("RI", "Rhode Island"),
    ("SC", "South Carolina"),
    ("SD", "South Dakota"),
    ("TN", "Tennessee"),
    ("TX", "Texas"),
    ("UT", "Utah"),
    ("VT", "Vermont"),
    ("VA", "Virginia"),
    ("WA", "Washington"),
    ("WV", "West Virginia"),
    ("WI", "Wisconsin"),
    ("WY", "Wyoming"),
]

# app.py
# Description: Main application file for Park Buddies, responsible for routing and rendering templates
# Todo: Refactor into smaller files: __init__.py, forms.py, models.py, nps_api.py, app_lists.py
# Todo: Add environment variables for Flask secret key and database URI


app = Flask(__name__)
db = SQLAlchemy()
app.secret_key = "PC_LOAD_LETTER"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/login.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def add_user(email, password, state):
    user = UserModel()
    user.set_password(password)
    user.email = email
    user.state = state
    db.session.add(user)
    db.session.commit()


def create_table():
    db.drop_all()
    db.create_all()
    user = UserModel.query.filter_by(email="lhhung@uw.edu").first()
    if user is None:
        add_user("lhhung@uw.edu", "qwerty", "WA")


@app.route("/")
def index():
    title = "Park Buddies"
    technology_dict = {
        "Python": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/110px-Python-logo-notext.svg.png",
        "Docker": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f4/Docker_logo.svg/512px-Docker_logo.svg.png",
        "Flask": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Flask_logo.svg/460px-Flask_logo.svg.png",
        "Nginx": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Nginx_logo.svg/320px-Nginx_logo.svg.png",
        "Bootstrap": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Bootstrap_logo.svg/301px-Bootstrap_logo.svg.png",
        "Gunicorn": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Gunicorn_logo_2010.svg/320px-Gunicorn_logo_2010.svg.png",
        "Amazon Web Services": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Amazon_Web_Services_Logo.svg/320px-Amazon_Web_Services_Logo.svg.png",
        "National Park Service": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Logo_of_the_United_States_National_Park_Service.svg/184px-Logo_of_the_United_States_National_Park_Service.svg.png",
        "Stack Overflow": "https://upload.wikimedia.org/wikipedia/commons/0/02/Stack_Overflow_logo.svg",
    }
    return render_template("index.html", title=title, tech=technology_dict)


@app.route("/home", methods=["GET", "POST"])
def home():
    title = "Home App"
    services = {
        "Activities": {
            "image": "goofy_camping_500x500.jpg",
            "btn": "Find your activities",
            "endpoint": "activities",
        },
        "Parks by State": {
            "image": "yakko_50states_384x384.jpg",
            "btn": "Find your parks",
            "endpoint": "parkbystate",
        },
        "Webcams": {
            "image": "monkey_selfie_555x555.jpg",
            "btn": "Observe your parks",
            "endpoint": "webcam",
        },
    }
    return render_template("home.html", title=title, services=services)


@app.route("/about")
def about():
    title = "About Us"
    profiles = {
        "Kevin Chung": {
            "gif": "https://media.giphy.com/media/l1J9DoKrzHMW8fP3O/giphy.gif",
            "endpoint": "webcam",
            "feat": [
                "User login, registration, and setting",
                "National Park API and webcams",
                "Docker and Bootstrap",
            ],
        },
        "Xingguo Huang": {
            "gif": "https://media.giphy.com/media/1wh06XT53tPGw/giphy.gif",
            "endpoint": "parkbystate",
            "feat": ["Parks by state", "Map widget", "Image carousel"],
        },
        "JP Montagnet": {
            "gif": "https://media.giphy.com/media/DfbpTbQ9TvSX6/giphy.gif",
            "endpoint": "activities",
            "feat": [
                "Park activites",
                "Multi-select query",
                "Official in house Software dev",
            ],
        },
    }
    site = [
        "Search all US National Parks by State.",
        "Determine which activities are available.",
        "Enjoy a live webcam feed directly with our service.",
        "Make edits to your user profile.",
    ]
    return render_template("about.html", title=title, profile=profiles, site=site)


def _activs_parks_xform(data):
    """
    Response data structure is... inconvenient:
    [ { id: <Activity1_id>, name: <Activity1_name>, parks:
        [ { parkCode: <Park1_code>, fullName: <Park1_name>, ... },
          { parkCode: <Park2_code>, fullName: <Park2_name>, ... },
          ... ] },
      { id: <Activity2_id>, name: <Activity2_name>, parks:
        [ { parkCode: <ParkX_code>, fullName: <ParkX_name>, ... },
        [ { parkCode: <ParkY_code>, fullName: <ParkY_name>, ... },
          ... ] },
      ... ]
    Parks info is repeated under every actiity applicable to it.

    Restructure to something more convenient:
    [ { "id": <Park1_code>,
        "name": <Park1_name>,
        "acts": { <Activity1_name>: <bool>,
                  <Activity2_name>: <bool>,
                  ... }},
      { "id": <Park2_code>,
        "name": <Park2_name>,
        "acts": { <Activity1_name>: <bool>,
                  ... }},
      ... ]

    A more compact representation is certainly possible,
    but the above strikes a reasonable balance.
    """
    if data is None:
        return None

    r = {}
    a_names = [x["name"] for x in data]
    for activ in data:
        a_name = activ["name"]
        for park in activ["parks"]:
            p_id = park["parkCode"]
            if p_id not in r:
                r[p_id] = {"name": park["fullName"], "acts": {}}
            r[p_id]["acts"][a_name] = True
    for a_name in a_names:
        for p_id in r.keys():
            if a_name not in r[p_id]["acts"]:
                r[p_id]["acts"][a_name] = False

    results = [{"id": k, "name": v["name"], "acts": v["acts"]} for k, v in r.items()]
    print(f"results = {r}")
    return results


@app.route("/activities", methods=["GET", "POST"])
def activities():
    title = "Park by Activities"
    form = ActivitiesForm()

    # Available choices, structured as required for SelectField
    # Canned example, a subset of the full set offered by API:
    # choices = [
    #  ('A59947B7-3376-49B4-AD02-C0423E08C5F7', 'Camping'),
    #  ('AE42B46C-E4B7-4889-A122-08FE180371AE', 'Fishing'),
    #  ('BFF8C027-7C8F-480B-A5F8-CD8CE490BFBA', 'Hiking'),
    #  ('F9B1D433-6B86-4804-AED7-B50A519A3B7C', 'Skiing')]
    choices = list_activities()
    form.activs.choices = choices

    # Subset of choices, as needed to both query the API (by id)
    # and to generate results table (by name).
    # Note structure here is dict, rather than list of tuples.
    # Canned example:
    # chosen = {
    #     'A59947B7-3376-49B4-AD02-C0423E08C5F7': 'Camping',
    #     'AE42B46C-E4B7-4889-A122-08FE180371AE': 'Fishing'}
    chosen = {}

    # Results from query of API, restructured for convenience.
    # Canned example:
    # results = {
    #   'jlst': { 'Name': 'Jellystone', 'Camping': True,  'Fishing': False },
    #   'atls': { 'Name': 'Atlantis',   'Camping': False, 'Fishing': True  }}
    results = {}

    if request.method == "GET":
        chosen_ids = chosen.keys()
        form.activs.data = chosen_ids
    elif form.validate_on_submit():
        chosen_ids = request.form.getlist("activs")
        chosen = dict([x for x in choices if x[0] in chosen_ids])
        data = activities_parks(ids=chosen_ids)
        results = _activs_parks_xform(data)
        # First sort by name
        r2 = sorted(results, key=lambda x: x["name"])
        results = r2
        # Then by largest match subset
        r2 = sorted(results, key=lambda x: -len([1 for a in x["acts"].values() if a]))
        results = r2
    return render_template(
        "activities.html", title=title, form=form, chosen=chosen, results=results
    )


@app.route("/webcam")
def webcam():
    title = "Active Park Webcams"
    return render_template("webcam.html", title=title, cams=webcams())


# @app.route("/settings", methods=["GET", "POST"])
# def settings():
#     title = "User Settings"
#     form = SettingsForm()

#     if request.method == "GET":
#         form.email.data = current_user.email
#         form.state.data = current_user.state

#     if request.method == "POST":
#         if form.validate_on_submit():
#             user = UserModel.query.filter_by(id=current_user.id).first()
#             pw = request.form["password"]

#             if user.check_password(pw):
#                 if request.form["state"] != user.state:
#                     flash("State changed successfully.", category="success")
#                     user.state = request.form["state"]
#                 if request.form["email"] != user.email:
#                     flash("Email changed successfully.", category="success")
#                     user.email = request.form["email"]
#                 if request.form["new_password"]:
#                     flash("Password changed successfully.", category="success")
#                     password_change = request.form["new_password"]
#                     user.set_password(password_change)

#                 db.session.commit()
#                 return render_template(
#                     "settings.html", title=title, user=current_user, form=form
#                 )
#             else:
#                 flash(
#                     f"Settings not applied. Incorrect credentials for {current_user.email}",
#                     category="warning",
#                 )
#     return render_template("settings.html", title=title, user=current_user, form=form)


@app.route("/parkbystate", methods=["GET", "POST"])
def parkbystate():
    title = "Park by State"
    form = searchForm()

    if form.validate_on_submit():
        if request.method == "POST":
            state = request.form["state"]
            return render_template(
                "parkbystate.html",
                title=title,
                myData=parks(state_code=state),
                form=form,
            )

    return render_template(
        "parkbystate.html",
        title=title,
        myData=parks(state_code=current_user.state),
        form=form,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    title = "Login Page"
    form = LoginForm()

    if form.validate_on_submit():
        if request.method == "POST":
            email = request.form["email"]
            pw = request.form["password"]
            user = UserModel.query.filter_by(email=email).first()
            if user is None:
                flash(
                    f"No account found. Please register for an account with our service.",
                    category="warning",
                )
            elif user and not user.check_password(pw):
                flash(
                    f"Incorrect password. Please try again.",
                    category="warning",
                )
            elif user and user.check_password(pw):
                flash(f"Welcome to Park Buddies!", category="success")
                return redirect(url_for("home"))
    return render_template("login.html", title=title, form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    title = "Registration Page"
    form = RegisterForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            state = request.form["state"]
            user = UserModel.query.filter_by(email=email).first()
            if user is None:
                add_user(email, password, state)
                flash("Registration successful.", category="success")
                return redirect(url_for("login"))
            elif user and user.check_password(password):
                flash("Registered account found.", category="success")
                return redirect(url_for("home"))
            else:
                flash(
                    "Email has already been taken. Please try another email.",
                    category="warning",
                )
    return render_template("register.html", title=title, form=form)


@app.route("/logout")
def logout():
    flash("Logout successful.", category="success")
    return redirect(url_for("login"))


@app.errorhandler(401)
def forbidden(e):
    title = "Unauthorized Access"
    return render_template("401.html", title=title), 401


@app.errorhandler(403)
def access_denied(e):
    title = "Forbidden Access"
    return render_template("403.html", title=title), 403


@app.errorhandler(404)
def page_not_found(e):
    title = "Page Not Found"
    return render_template("404.html", title=title), 404


# forms.py
# Desc: Forms for user login, registration, and settings.
# Todo: Add form for activities search. Remove login and registration forms from app.py


class LoginForm(FlaskForm):
    """
    Form to collect existing user credentials.
    """

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        label="Password", validators=[DataRequired(), Length(min=6, max=16)]
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    """
    Form to collect new user information that will be added to the database.
    """

    email = StringField("Enter email", validators=[DataRequired(), Email()])
    state = SelectField("Select state", choices=STATE_LIST, validators=[DataRequired()])
    password = PasswordField(
        "Enter password", validators=[DataRequired(), Length(min=6, max=16)]
    )
    password2 = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match!"),
        ],
    )
    submit = SubmitField(label="Register")


class searchForm(FlaskForm):
    # state = SelectField('Choose a state!', choices=['WA', 'OR', 'CA'], validators=[DataRequired()])
    state = SelectField(
        "Choose a State for Details", choices=STATE_LIST, validators=[DataRequired()]
    )
    submit = SubmitField(label="Search")


class SettingsForm(FlaskForm):
    """
    Form to change existing user settings.
    """

    email = StringField("Change email", validators=[Email(), DataRequired()])
    state = SelectField("Change state", choices=STATE_LIST, validators=[Optional()])
    new_password = PasswordField(
        label="Change password", validators=[Length(min=6, max=16), Optional()]
    )
    password = PasswordField(
        label="Re-enter current password to confirm updates",
        validators=[DataRequired(), Length(min=6, max=16)],
    )
    submit = SubmitField("Update")


class ActivitiesForm(FlaskForm):
    """
    Form to collect parameters for activities search.
    """

    # activs = SelectMultipleField("Activities", validators=[DataRequired()])
    activs = SelectMultipleField("Activities", validators=[Optional()])
    submit = SubmitField(label="Search")


# models.py
# Description: ORM tables to be used with SQLAlchemy, and Flask-Login
# Todo: remove references to db and login, and move to a separate file


db = SQLAlchemy()


class UserModel(db.Model):
    """
    Base ORM table to be used with SQLAlchemy
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(2), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(), nullable=False)

    def set_password(self, password):
        """
        Security measure to ensure no passwords are hard coded within the application.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Security measuer to validate passwords within a database.
        """
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=robohash&s={size}"

    def __repr__(self):
        return f"{self.id} | {self.state} | {self.email}"


# nps_api.py


base_url = f"https://developer.nps.gov/api/v1/"
params = {"api_key": "rRScznr5cMqmr00eoeO61Xmc3FL9fB6o499OJqbf"}


def activities_api():
    """Retrieve categories of activities (astronomy, hiking, wildlife watching, etc.) possible in national parks. dict: all activities codified by NPS"""
    request_url = base_url + "activities"
    response = requests.get(request_url, params=params)
    data = response.json()["data"]

    # Restructure as list of tuples (id, name), consistent with wtforms
    # SelectField choices, i.e. list of tuples (value, label).
    results = [(_x["id"], _x["name"]) for _x in data]
    return results


def activities_parks(ids: list[str], qry: str) -> list:
    """Retrieve national parks that are related to particular categories
    of activity (astronomy, hiking, wildlife watching, etc.).

    Returns:
        dict: all activities codified by NPS with associated parks
    """
    if not ids and (not qry or qry == ""):
        return []

    global params
    request_url = base_url + "activities/parks"
    p = params.copy()
    if ids is not None and ids != "":
        # XXX gross workaround: NPS API requires that multiple "id" values
        # be passed as a single string formatted as comma-separated list;
        # it does not support the standard alternative of multiple "id" params.
        # Meanwhile, Python requests library insists on URL-encoding everything
        # in params dict; and furthermore, thinks comma needs to be encoded.
        # This encoding can be circumvented by including query-string in URL.
        # Additional params can still be specified and will be correctly
        # appended with ampersand instead of question-mark.
        # p["id"] = ids
        request_url = f"{request_url}?id={','.join(ids)}"
    if qry is not None and qry != "":
        p["q"] = qry
    response = requests.get(request_url, params=p)
    return response.json()["data"]


def parks(state_code: str, park_code: str):
    """Retrieve data about national parks (addresses, contacts, description, hours of operation, etc.).

    Args:
        state_code (str, optional): A comma delimited list of 2 character state codes. Defaults to None.
        park_code (str, optional): A comma delimited list of park codes (each 4-10 characters in length). Defaults to None.

    Returns:
        dict: all parks listed in the US
    """
    params["limit"] = "500"
    params["parkCode"] = park_code
    params["stateCode"] = state_code
    request_url = base_url + "parks"

    response = requests.get(request_url, params=params)
    data = response.json()["data"]

    parks = {x["parkCode"]: x for x in data}
    for parkCode in parks.items():
        parks[parkCode[0]]["address"] = _address_string(parkCode[1]["addresses"][0])
    return parks


def webcams():
    """Retrieve metadata about National Park Service streaming and non-streaming web cams.

    Returns:
        dict: all activities codified by NPS with associated parks
    """
    params["limit"] = "500"
    request_url = base_url + "webcams"

    response = requests.get(request_url, params=params)
    data = response.json()["data"]

    webcam_data = {
        x["relatedParks"][0]["parkCode"]: x
        for x in data
        if x["status"] == "Active" and x["relatedParks"] and len(x["images"]) > 0
    }
    webcams = _webcam_scrub(webcam_data)

    return webcams


def _address_string(addresses: dict):
    return f"{addresses['line1']}, {addresses['city']}, {addresses['stateCode']} {addresses['postalCode']}"


def _webcam_scrub(park_cams: dict):
    """
    Helper function to update related data for the Flask webpage
    """
    ref_parks = parks()
    new_dict = {key: ref_parks[key] for key in park_cams.keys() if key in ref_parks}
    x = 0

    for key, value in park_cams.items():
        new_images = new_dict[key]["images"]
        for image in new_images:
            park_cams[key]["images"].append(image)

        related = value.pop("relatedParks")[0]
        park_cams[key]["webpage"] = related.pop("url")
        park_cams[key].update(related)

    return park_cams


# wsgi.py
#!/usr/bin/env python
# Entry point for the application in production environment
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
