import random
from app.model import db, User
from flask import request, redirect, url_for,render_template, Blueprint, jsonify, make_response, make_response
from functools import wraps
import jwt
import uuid
from datetime import datetime, timedelta
from  werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies


auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route("/")
def index():
    return render_template("login.html")

@auth.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        auth = request.form
        user = User.query\
        .filter_by(email = auth.get('email'))\
        .first()

        if not auth or not auth.get('email') or not auth.get('password'):
        # return if input field is empty
            return redirect(url_for("auth.showAddForm"))

        if not user:
        # returns 401 if user does not exist
            return redirect(url_for('auth.showAddForm'))
        
        if check_password_hash(user.password, auth.get('password')):
            # generates the JWT Token
            response = make_response(redirect(url_for("admin.home")))
            additional_claims = {"uuid":user.public_id}
            access_token = create_access_token(identity=user.email, additional_claims=additional_claims)
            set_access_cookies(response, access_token)
            return response
        # returns 403 if password is wrong
        return redirect(url_for('auth.showAddForm'))

@auth.route("/showAddForm")
def showAddForm():
    return render_template("adduser.html")

@auth.route('/signup', methods=["POST"])
def signup():
    if request.method == "POST":
        data = request.form

        #get name , email and password
        name, email = data.get('name'), data.get("email")
        password = data.get('password')
        password2 = data.get('password2')

        #checking if password and confirm password is the same
        if password != password2:
            return redirect(url_for('auth.showAddForm'))
        
        #checking for exisiting user
        user = User.query.filter_by(email=email).first()
        if not user:
            #database ORM object
            user = User(
                public_id = str(random.seed(uuid.uuid4)),
                name = name,
                email = email, 
                password = generate_password_hash(password, method='pbkdf2:sha1', salt_length=4)
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.index'))
        else:
             # returns 202 if user already exists
            return make_response('User already exists. Please Log in.', 202)
