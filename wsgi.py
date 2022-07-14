from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required

from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
# initiating SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///./main.db'
app.config["SQLALCHEMY_ECHO"] = True

# configuring JWTManager
app.config["JWT_SECRET_KEY"] = 'WMZhnxvKcrwMs3Een9YPaXVyMnHtihkjxLriuPNRGhhU9vdHWGyn7bYbOcmOFfJ4RvBdFg'

class User(db.Model):
    __tablename__ = "user_detail"

    id = db.Column(db.Integer,primary_key = True, autoincrement =True)
    email = db.Column(db.String(255), unique = True)
    password = db.Column(db.String(22), nullable=False)
    reg_date_time = db.Column(db.DateTime, nullable=False)



# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.email


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(email=identity).one_or_none()

# db.create_all()
# if you have to use the application in console you can use the following command
# from app_name import *
# app.app_context().push()
# after this you can use all the common python command in console for the application

@app.route("/")
def index():
    return jsonify(
        status = True,msg = "I am best at flask"
    )

@app.route("/register", methods=["POST"])
def register():
    try:# plan A
        email = request.form.get("email")
        password = request.form.get("password")

        new_user = User(email = email, password = password, reg_date_time  = datetime.now())

        # adding to the session
        db.session.add(new_user)
        # commiting the change to the database
        db.session.commit()
        return jsonify(status = True, msg="user registered successfully")
    except IntegrityError as error_obj:
        print(error_obj)
        return jsonify(status = False, msg="Something went wrong!")


@app.route("/login", methods=["POST"])
def login():
    try:
        user_email = request.form.get("email")
        user_password = request.form.get("password")

        # "SELECT * FROM user_detail WHERE email=%s"(user_email)
        expected_user = User.query.filter_by(email = user_email).one_or_none()
        if expected_user is not None:
            if expected_user.password == user_password:
                access_token = create_access_token(identity = expected_user)
                return jsonify(status = True, msg="logged in", access_token = access_token)
        return jsonify(status = False, msg="User Id or Password didn't matched.")
    except: 
        return jsonify(status=False, msg="Something went worng")



@app.route("/dummy")
@jwt_required()
def dummy():
    return jsonify(status=True)