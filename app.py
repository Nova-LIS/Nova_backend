from flask import Flask,render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS

db=SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY']='0099734a1b530d8a8de2f3b7d091b60c'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site2.db'
db.init_app(app)

CORS(app)

class User(db.Model):
    name = db.Column(db.String(50),nullable=False,unique=False)
    roll = db.Column(db.String(10), nullable=False, unique=True)
    designation = db.Column(db.String(15), nullable=False, unique=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    phone=db.Column(db.Integer,unique=True,nullable=False)
    username=db.Column(db.String(20),unique=True,primary_key=True)
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
    booknumber=db.Column(db.Integer)
    bookid=db.Column(db.Integer,primary_key=True)
    isbn=db.Column(db.String(),nullable=False)
    author=db.Column(db.String(80),nullable=False)
    published_date=db.Column(db.String(),nullable=False)
    title=db.Column(db.String(100),nullable=False,unique=True)
    # description=db.Column(db.String())
    # publisher=db.Column(db.String())
    # page_count=db.Column(db.Integer)
    # genres=db.Column(db.String(),nullable=False)
    image_url=db.Column(db.String(),nullable=False)
    small_image_url=db.Column(db.String(),nullable=False)
    no_of_copies=db.Column(db.Integer,nullable=False)
    racknumber=db.Column(db.Integer,nullable=False)

    # def __repr__(self):
    #     return f"User('{self.bo}','{self.isbn}','{self.author}','{self.copies}'," \
    #            f"'{self.last_issued}')"

    def __init__(self,booknumber,title,author,description,publisher,page_count,genres,isbn,published_date,no_of_copies,racknumber):
        self.booknumber=booknumber
        self.title = title
        self.author=author
        self.description=description
        self.publisher=publisher
        self.page_count=page_count
        self.genres=genres
        self.isbn=isbn
        self.published_date=published_date
        self.no_of_copies=no_of_copies
        self.racknumber=racknumber

class issueRecord(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    bookissued=db.Column(db.Integer,db.ForeignKey('book.booknumber'),nullable=False)
    issuedto=db.Column(db.String(),db.ForeignKey('user.username'),nullable=False)
    issuedate=db.Column(db.String(),nullable=False)
    expectedreturn=db.Column(db.String(),nullable=False)
    isOverdue=db.Column(db.Integer,default=0,nullable=False)
    overdueDuration=db.Column(db.Integer,default=0,nullable=False)

    def __init__(self,bookissued,issuedto,issuedate,expectedreturn,isOverdue,overdueDuration):
        self.bookissued=bookissued
        self.issuedto=issuedto
        self.issuedate=issuedate
        self.expectedreturn=expectedreturn
        self.isOverdue=isOverdue
        self.overdueDuration=overdueDuration


@app.route('/about',methods=['GET','POST'])
def about():
    return render_template('./about.html',title='About')


@app.route('/register',methods=['GET','POST'])
def register():    
    name=request.json['name']
    roll=request.json['roll']
    email=request.json['email']
    phone=int(request.json['phone'].strip())
    username=request.json['userName']
    password=request.json['password']
    record = User(name,roll,email,phone,username,password)

    roll_exists = User.query.filter_by(roll=roll.strip()).first()
    email_exists = User.query.filter_by(email=email.strip()).first()
    phone_exists = User.query.filter_by(phone=phone).first()
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
                "isPasswordCorrect": True,
                "name": user.name,
                "roll": user.roll,
                "designation": user.designation,
                "phone": 19821212,
                "email": user.email,
                "userName": user.username
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

@app.route('/browse',methods=['GET','POST'])
def browse():
    bookname=request.json["bookname"]
    bookdata=[]
    flag=0
    for book in Book.query.filter(Book.title.contains(bookname)):
        flag=1
        bookdata.append({
            "foundBook":True,
            "title":book.title,
            "author":book.author,
            "description":book.description,
            "publisher":book.publisher,
            "page_count":book.page_count,
            "genres":book.genres,
            "isbn":book.isbn,
            "published_date":book.published_date,
            "no_of_copies":book.no_of_copies,
            "racknumber":book.racknumber,
        })
    if flag==0:
        data={
            "foundBook":False
        }
        return jsonify(data)
    else:
        return jsonify(bookdata)


@app.route('/issue',methods=['GET','POST'])
def issuebook():
    booknumber=request.json["booknumber"]
    bookdata=[]
    
    # if book:
    #     if user.password == password:
    #         data = {
    #             "isRegistered": True,     
    #             "isPasswordCorrect": True
    #         }
    #     else:
    #         data = {
    #             "isRegistered": True,          
    #             "isPasswordCorrect": False
    #         }
    #     return jsonify(data)
    # else:
    #     data = {
    #         "isRegistered": False
    #     }
    #     return jsonify(data)




if __name__=='__main__':
    app.run(debug=True)




