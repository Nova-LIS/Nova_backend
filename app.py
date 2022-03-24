from ast import JoinedStr, Return
from cmath import log
from distutils.log import error
from enum import unique
from genericpath import exists
from lib2to3.pytree import Base
from flask import Flask,render_template,flash,url_for,redirect,request,jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_marshmallow import Marshmallow
# from forms import RegistrationForm,LoginForm
from flask_cors import CORS

db=SQLAlchemy()
# migrate = Migrate()
# ma = Marshmallow()
#cors = CORS()
app = Flask(__name__)
app.config['SECRET_KEY']='0099734a1b530d8a8de2f3b7d091b60c'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site2.db'
db.init_app(app)
CORS(app)

class User(db.Model):
    name = db.Column(db.String(50),nullable=False,unique=True)
    roll = db.Column(db.String(10), nullable=False, unique=True)
    email=db.Column(db.String(100),unique=True,nullable=False)
    phone=db.Column(db.Integer,unique=True,nullable=False)
    username=db.Column(db.String(20),primary_key=True)
    password=db.Column(db.String(30),nullable=False)

    def __repr__(self):
        return f"User('{self.name}','{self.roll}','{self.email}','{self.phone}','{self.username}')"

    def __init__(self,name, roll, email,phone, username,password):
        self.name = name
        self.roll = roll
        self.email = email
        self.phone = phone
        self.username = username
        self.password=password

    def serialize(self):
        return {"name": self.name,
                "roll": self.roll,
                "email": self.email,
                "phone":self.phone,
                "username":self.username,
                "password":self.password}


class Book(db.Model):
    name=db.Column(db.String(50),nullable=False,unique=True)
    isbn=db.Column(db.String(13),primary_key=True)
    author=db.Column(db.String(50),nullable=False)
    copies=db.Column(db.Integer,default=1)
    last_issued=db.Column(db.Integer,default=0)

    def __repr__(self):
        return f"User('{self.name}','{self.isbn}','{self.author}','{self.copies}'," \
               f"'{self.last_issued}')"

    def __init__(self,name, isbn, author,copies,last_issued):
        self.name = name
        self.isbn=isbn
        self.author=author
        self.copies=copies
        self.last_issued=last_issued


@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
def home():
    return render_template('./home.html',title='Home')


@app.route('/about',methods=['GET','POST'])
def about():
    return render_template('./about.html',title='About')


@app.route('/register',methods=['GET','POST'])
def register():

    #input_json = request.get_json(force=True)
    #print(input_json)
    
    name=request.json['name']
    roll=request.json['roll']
    email=request.json['email']
    phone=int(request.json['phone'])
    username=request.json['userName']
    password=request.json['password']
    record = User(name,roll,email,phone,username,password)

    roll_exists = User.query.filter_by(roll=roll.strip()).first()
    email_exists = User.query.filter_by(email=email.strip()).first()
    phone_exists = User.query.filter_by(phone=phone.strip()).first()
    username_exists = User.query.filter_by(username=username.strip()).first()

    exists = roll_exists or email_exists or phone_exists or username_exists

    if exists:
        data = {
            "accepted": False,
            "rollExists": True if roll_exists else False,
            "emailExists": True if email_exists else False,
            "phoneExists": True if phone_exists else False,
            "usernameExists": True if username_exists else False,               
        }
        return jsonify(data)

    else:
        db.session.add(record)
        db.session.commit()
        data = {
            "accepted": True,
            "rollExists": False,
            "emailExists": False,
            "phoneExists": False,
            "usernameExists": False,    
        }
        return jsonify(data)


@app.route('/login',methods=['GET','POST'])
def login():
    username = request.json["userName"]
    password = request.json["password"]

    user = User.query.filter_by(username=username.strip()).first()


    if user:
        if user.password == password:
            data = {
                "isRegistered": True,     
                "isPasswordCorrect": True
            }
        else:
            data = {
                "isRegistered": True,          
                "isPasswordCorrect": False
            }
        return jsonify(data)
    else:
        data = {
            "isRegistered": False
        }
        return jsonify(data)


if __name__=='__main__':
    app.run(debug=True)
    # migrate.init_app(app, db)
    # ma.init_app(app)





