from flask import Flask,render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta

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

    def __init__(self,name, roll, email,phone, username,password,designation):
        self.name = name
        self.roll = roll
        self.email = email
        self.phone = phone
        self.username = username
        self.password=password
        self.designation=designation

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

    def __init__(self,booknumber,bookid,isbn,author,published_date,title,image_url,small_image_url,no_of_copies,racknumber):
        booknumber=db.Column(db.Integer)
        bookid=db.Column(db.Integer,primary_key=True)
        isbn=db.Column(db.String(),nullable=False)
        author=db.Column(db.String(80),nullable=False)
        published_date=db.Column(db.String(),nullable=False)
        title=db.Column(db.String(100),nullable=False,unique=True)
        image_url=db.Column(db.String(),nullable=False)
        small_image_url=db.Column(db.String(),nullable=False)
        no_of_copies=db.Column(db.Integer,nullable=False)
        racknumber=db.Column(db.Integer,nullable=False)

class Issuerecord(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    bookissued=db.Column(db.Integer,db.ForeignKey('book.booknumber'),nullable=False)
    issuedto=db.Column(db.String(),db.ForeignKey('user.username'),nullable=False)
    issuedate=db.Column(db.String(),nullable=False)
    expectedreturn=db.Column(db.String(),nullable=False)
    # isOverdue=db.Column(db.Integer,default=0,nullable=False)
    # overdueDuration=db.Column(db.Integer,default=0,nullable=False)
    returned=db.Column(db.Integer,default=0,nullable=False)
    returndate=db.Column(db.String())

    def __init__(self,id,bookissued,issuedto,issuedate,expectedreturn,returned,returndate=""):
        self.id=id
        self.bookissued=bookissued
        self.issuedto=issuedto
        self.issuedate=issuedate
        self.expectedreturn=expectedreturn
        # self.isOverdue=isOverdue
        # self.overdueDuration=overdueDuration
        self.returned=returned
        self.returndate=returndate

    def isOverdue(self):
        now = datetime.now()
        expectedreturn = datetime.strptime(self.expectedreturn, '%Y-%m-%d %H:%M:%S.%f')
        return (expectedreturn<now)
    
    def overdueDuration(self):
        if(self.isOverdue()):
            now = datetime.now()
            expectedreturn = datetime.strptime(self.expectedreturn, '%Y-%m-%d %H:%M:%S.%f')
            return (now-expectedreturn).days+1
        else:
            return 0

            # def printReminder(self):
    #     if(self.isOverdue()):
    #         overshoot = self.overdueDuration()
    #         return jsonify({"isOverdue":1,"overdueDuration":overshoot})
    #     else:
    #         return jsonify({"isOverdue":0})

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
    designation=request.json['designation']
    print(designation)
    record = User(name,roll,email,phone,username,password,designation)

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
            booksissued=[]
            for record in Issuerecord.query.filter_by(issuedto=username):
                bookid=record.bookissued
                book=Book.query.filter_by(bookid=bookid).first()
                booksissued.append(
                    {
                        "booknumber":book.booknumber,
                        "bookid":book.bookid,
                        "isbn":book.isbn,
                        "author":book.author,
                        "published_date":book.published_date,
                        "title":book.title,
                        "image_url":book.image_url,
                        "small_image_url":book.small_image_url,
                        "no_of_copies":book.no_of_copies,
                        "racknumber":book.racknumber,
                        "issueid":record.id,
                        "issuedate":record.issuedate,
                        "expectedreturn":record.expectedreturn,
                        "isOverdue":record.isOverdue,
                        "overdueDuration":record.overdueDuration,
                        "returned":record.returned
                    })
            data = {
                "isRegistered": True,     
                "isPasswordCorrect": True,
                "name": user.name,
                "roll": user.roll,
                "designation": user.designation,
                "phone": user.phone,
                "email": user.email,
                "userName": user.username,
                "booksissued":booksissued
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

@app.route('/profile/<string:username>',methods=['GET'])
def getIssuedBooks(username):
    booksissued=[]
    for record in Issuerecord.query.filter_by(issuedto=username):
        bookid=record.bookissued
        book=Book.query.filter_by(bookid=bookid).first()
        booksissued.append({
        "booknumber":book.booknumber,
        "bookid":book.bookid,
        "isbn":book.isbn,
        "author":book.author,
        "published_date":book.published_date,
        "title":book.title,
        "image_url":book.image_url,
        "small_image_url":book.small_image_url,
        "no_of_copies":book.no_of_copies,
        "racknumber":book.racknumber,
        "issuedate":record.issuedate,
        "expectedreturn":record.expectedreturn,
        "isOverdue":record.isOverdue,
        "overdueDuration":record.overdueDuration,
        "returned":record.returned
    })
    return jsonify(booksissued)


@app.route('/browse',methods=['GET','POST'])
def browse():
    bookname=request.json["bookname"]
    books=[]
    flag=0
    for book in Book.query.filter(Book.title.contains(bookname)):
        flag=1
        books.append({
            "bookid":book.bookid,
            "booknumber":book.booknumber,
            "title":book.title,
            "author":book.author,
            "isbn":book.isbn,
            "published_date":book.published_date,
            "image_url":book.image_url,
            "small_image_url":book.small_image_url,
            "no_of_copies":book.no_of_copies,
            "racknumber":book.racknumber
        })
    if flag==0:
        data={
            "foundBook":False
        } 
        return jsonify(data)
    else:
        data={
            "foundBook":True,
            "books":books
        }
        return jsonify(data)

@app.route('/book/<int:number>')
def getBook(number):
    book = Book.query.filter_by(booknumber=int(number)).first()
    serialBook = {
        "bookid":book.bookid,
        "booknumber":book.booknumber,
        "title":book.title,
        "author":book.author,
        "isbn":book.isbn,
        "published_date":book.published_date,
        "image_url":book.image_url,
        "small_image_url":book.small_image_url,
        "no_of_copies":book.no_of_copies,
        "racknumber":book.racknumber
    }
    return jsonify(serialBook)


@app.route('/issue',methods=['GET','POST'])
def issuebook():
    bookid=request.json["bookid"]
    username=request.json["username"]
    issueentry=[]
    record=Issuerecord.query.filter(bookissued=bookid, issuedto=username, returned=0)
    if record:
        return jsonify({"alreadyissued": True})
    bookissue=Book.query.filter_by(bookid=bookid).first()
    userissue=User.query.filter_by(username=username.strip()).first()
    if (bookissue.no_of_copies>0):
        date=datetime.now()
        data = {
            "isIssued": True,
        }
        issueDuration=0
        if(userissue.designation=="UG Student"):
            issueDuration=30
        elif(userissue.designation=="PG Student"):
            issueDuration=60
        elif(userissue.designation=="Research Scholar"):
            issueDuration=90
        else:
            issueDuration=180
        issueid=db.session.query(Issuerecord).count()
        bookissue.no_of_copies-=1
        issueEntry=Issuerecord(issueid+1,bookissue.bookid,userissue.username,date,date+timedelta(days=issueDuration),0)
        db.session.add(issueEntry)
        db.session.commit()
        return jsonify(data)
    data={
        "isIssued":False,
    }
    return jsonify(data)

@app.route('/return',methods=['GET','POST'])
def returnBook():
    bookid=request.json["bookid"]
    username=request.json["username"]

if __name__=='__main__':
    app.run(debug=True)




