from flask import Flask,render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime,timedelta
import random

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
    booksissued=db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"User('{self.name}','{self.roll}','{self.email}','{self.phone}','{self.username}')"

    def __init__(self,name, roll, email,phone, username,password,designation,booksissued):
        self.name = name
        self.roll = roll
        self.email = email
        self.phone = phone
        self.username = username
        self.password=password
        self.designation=designation
        self.booksissued=booksissued

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
    isbn=db.Column(db.Integer,nullable=False)
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
    isDeleted=db.Column(db.Integer)

    # def __repr__(self):
    #     return f"User('{self.bo}','{self.isbn}','{self.author}','{self.copies}'," \
    #            f"'{self.last_issued}')"

    def __init__(self,booknumber,bookid,isbn,author,published_date,title,image_url,small_image_url,no_of_copies,racknumber,isDeleted=0):
        self.booknumber=booknumber
        self.bookid=bookid
        self.isbn=isbn
        self.author=author
        self.published_date=published_date
        self.title=title
        self.image_url=image_url
        self.small_image_url=small_image_url
        self.no_of_copies=no_of_copies
        self.racknumber=racknumber
        self.isDeleted=isDeleted

class Issuerecord(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    bookid=db.Column(db.Integer,db.ForeignKey('book.bookid'),nullable=False)
    issuedto=db.Column(db.String(),db.ForeignKey('user.username'),nullable=False)
    issuedate=db.Column(db.String(),nullable=False)
    expectedreturn=db.Column(db.String(),nullable=False)
    # isOverdue=db.Column(db.Integer,default=0,nullable=False)
    # overdueDuration=db.Column(db.Integer,default=0,nullable=False)
    returned=db.Column(db.Integer,default=0,nullable=False)
    returndate=db.Column(db.String())
    isPrinted=db.Column(db.Integer)


    def __init__(self,id,bookid,issuedto,issuedate,expectedreturn,returned,returndate="",isPrinted=0):
        self.id=id
        self.bookid=bookid
        self.issuedto=issuedto
        self.issuedate=issuedate
        self.expectedreturn=expectedreturn
        # self.isOverdue=isOverdue
        # self.overdueDuration=overdueDuration
        self.returned=returned
        self.returndate=returndate
        self.isPrinted=isPrinted

    def isOverdue(self):
        now = datetime.now()
        expectedreturn = datetime.strptime(self.expectedreturn, '%Y-%m-%d %H:%M:%S.%f')
        issuedate = datetime.strptime(self.issuedate, '%Y-%m-%d %H:%M:%S.%f')
        return ((expectedreturn-issuedate).days<int((now-issuedate).total_seconds()))
    
    def overdueDuration(self):
        if(self.isOverdue()):
            now = datetime.now()
            expectedreturn = datetime.strptime(self.expectedreturn, '%Y-%m-%d %H:%M:%S.%f')
            issuedate = datetime.strptime(self.issuedate, '%Y-%m-%d %H:%M:%S.%f')
            expectedreturn_in_seconds=(expectedreturn-issuedate).days
            return int(((now-(issuedate+timedelta(seconds=expectedreturn_in_seconds))).total_seconds()))
        else:
            return 0

    def penalty(self):
        overdueDuration=self.overdueDuration()
        penalty=0
        if(overdueDuration):
            for i in range(1,overdueDuration,7):
                penalty+=(50*(int(i/7)+1))
        return penalty

            # def printReminder(self):
    #     if(self.isOverdue()):
    #         overshoot = self.overdueDuration()
    #         return jsonify({"isOverdue":1,"overdueDuration":overshoot})
    #     else:
    #         return jsonify({"isOverdue":0})

class Reserverecord(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    bookid=db.Column(db.Integer,nullable=False)
    username=db.Column(db.String(80),nullable=False)
    returndate=db.Column(db.String(),nullable=False,default="NULL")
    isavailable=db.Column(db.Integer,default=0)

    def __init__(self,id,bookid,username,returndate="NULL",isavailable=0):
        self.id=id
        self.bookid=bookid
        self.username=username
        self.returndate=returndate
        self.isavailable=isavailable

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
    record = User(name,roll,email,phone,username,password,designation,booksissued=0)

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

@app.route('/reserve',methods=["GET","POST"])
def reserveBook():
    bookid=request.json["bookid"]
    username=request.json["username"]
    id=db.session.query(Reserverecord).count()
    record=Reserverecord.query.filter_by(bookid=bookid,username=username).first()
    if(record):
        return jsonify({"alreadyReserved":True})
    reserveEntry=Reserverecord(id+1,bookid,username)
    db.session.add(reserveEntry)
    db.session.commit()
    return jsonify({"reserved":True})


@app.route('/login',methods=['GET','POST'])
def login():
    username = request.json["userName"]
    password = request.json["password"]
    user = User.query.filter_by(username=username.strip()).first()


    if user:
        if user.password == password:
            # booksissued=[]
            # for record in Issuerecord.query.filter_by(issuedto=username):
            #     bookid=record.bookissued
            #     book=Book.query.filter_by(bookid=bookid).first()
            #     booksissued.append(
            #         {
            #             "booknumber":book.booknumber,
            #             "bookid":book.bookid,
            #             "isbn":book.isbn,
            #             "author":book.author,
            #             "published_date":book.published_date,
            #             "title":book.title,
            #             "image_url":book.image_url,
            #             "small_image_url":book.small_image_url,
            #             "no_of_copies":book.no_of_copies,
            #             "racknumber":book.racknumber,
            #             "issueid":record.id,
            #             "issuedate":record.issuedate,
            #             "expectedreturn":record.expectedreturn,
            #             "isOverdue":record.isOverdue()
            #             "overdueDuration":record.overdueDuration()
            #             "returned":record.returned
            #         })
            data = {
                "isRegistered": True,     
                "isPasswordCorrect": True,
                "name": user.name,
                "roll": user.roll,
                "designation": user.designation,
                "phone": user.phone,
                "email": user.email,
                "userName": user.username,
                # "booksissued":booksissued
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
        bookid=record.bookid
        book=Book.query.filter_by(bookid=bookid).first()
        if book:
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
            "id":record.id,
            "issuedate":record.issuedate,
            "expectedreturn":record.expectedreturn,
            "isOverdue":record.isOverdue(),
            "overdueDuration":record.overdueDuration(),
            "returned":record.returned,
            "returndate":record.returndate,
            "isPrinted": record.isPrinted,
            "isDeleted":book.isDeleted,
        })

    booksreserved=[]
    now = datetime.now()
    for record in Reserverecord.query.filter_by(username=username):
        if(record.isavailable==1 and (int((now-datetime.strptime(record.returndate,'%Y-%m-%d %H:%M:%S.%f')).total_seconds())/60)*(7/5)>7):
            delrecord=record
            db.session.delete(delrecord)
            db.session.commit()
        else:
            book = Book.query.filter_by(bookid=record.bookid).first()
            booksreserved.append({
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
                "returndate":record.returndate,
                "username": username,
                "isAvailable": record.isavailable
            })
    return jsonify({"booksissued": booksissued, "booksreserved": booksreserved})


@app.route('/unreturnedBooks',methods=['GET','POST'])

def unreturnedBooks():
    booksissued=[]
    for record in Issuerecord.query.filter_by(returned=0):
        bookid=record.bookid
        book=Book.query.filter_by(bookid=bookid).first()
        booksissued.append({
        "title":book.title,
        "image_url":book.image_url,
        "small_image_url":book.small_image_url,
        "id":record.id,
        "issuedate":record.issuedate,
        "expectedreturn":record.expectedreturn,
        "isOverdue":record.isOverdue(),
        "username": record.issuedto,
        "isPrinted": record.isPrinted,
        "isDeleted": book.isDeleted
    })

    return jsonify(booksissued)

@app.route('/printReminder/<int:issueid>',methods=['GET','POST'])
def printReminder(issueid):
    record=Issuerecord.query.filter_by(id=issueid).first()
    print(record)
    #return jsonify({})
    if record.isPrinted == 1:
        return jsonify({"alreadySent": True})
    else:
        record.isPrinted = 1
        db.session.commit()
        return jsonify({"alreadySent": False})


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
            "racknumber":book.racknumber,
            "isDeleted":book.isDeleted
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

@app.route('/getUsers',methods=["GET"])
def getUsers():
    users=[]
    flag=0
    for user in User.query.all():
        flag=1
        users.append({
            "name":user.name,
            "username":user.username,
            "designation":user.designation
        })
    if(flag==1):
        data={
            "usersFound":True,
            "users":users
        } 
        return jsonify(data)
    else:
        data={
            "usersFound":False
        }
        return jsonify(data)

@app.route("/deleteUser/<string:username>", methods=["DELETE"])
def guide_delete(username):
    user=User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({"userDeleted":True})


@app.route('/issue',methods=['GET','POST'])
def issuebook():
    bookId=request.json["bookid"]
    username=request.json["username"]
    issueentry=[]
    record=Issuerecord.query.filter_by(bookid=bookId, issuedto=username, returned=0).first()
    if record:
        return jsonify({"alreadyissued": True})

    bookissue=Book.query.filter_by(bookid=bookId).first()
    userissue=User.query.filter_by(username=username.strip()).first()
    if(userissue.designation=="UG Student" and userissue.booksissued>=2):
        return jsonify({"issuelimit":True})
    elif(userissue.designation=="PG Student" and userissue.booksissued>=4):
        return jsonify({"issuelimit":True})
    elif(userissue.designation=="Research Scholar" and userissue.booksissued>=6):
        return jsonify({"issuelimit":True})
    elif(userissue.booksissued>=10):
        return jsonify({"issuelimit":True})
    issueDuration=0
    if(userissue.designation=="UG Student"):
        issueDuration=30
    elif(userissue.designation=="PG Student"):
        issueDuration=60
    elif(userissue.designation=="Research Scholar"):
        issueDuration=90
    else:
        issueDuration=180
    date=datetime.now()
    if (bookissue.no_of_copies>0):
    
        issueid=db.session.query(Issuerecord).count()
        bookissue.no_of_copies-=1
        db.session.commit()
        issueEntry=Issuerecord(issueid+1,bookissue.bookid,userissue.username,date,date+timedelta(days=issueDuration),0)
        db.session.add(issueEntry)
        db.session.commit()
        db.session.flush()
        data = {
            "isIssued": True,
            "id": issueEntry.id
        }
        userissue.booksissued+=1
        db.session.commit()
        return jsonify(data)
    else:
        flag=0
        for record in Reserverecord.query.filter_by(bookid=bookId):
            flag=1
            if(record.isavailable==1):
                if(int((date-datetime.strptime(record.returndate,'%Y-%m-%d %H:%M:%S.%f')).total_seconds()/60)*(7/5)>7):
                    delrecord=record
                    db.session.delete(delrecord)
                    db.session.commit()
                else:
                    break
        record=Reserverecord.query.filter_by(bookid=bookId,username=username).first()
        if(flag==1):
            record2=db.session.query(Reserverecord).filter(Reserverecord.username!=username).filter(Reserverecord.bookid==bookId).first()
        if((record and record.isavailable==1)or(flag==1 and record2 is None)):
            issueid=db.session.query(Issuerecord).count()
            db.session.commit()
            issueEntry=Issuerecord(issueid+1,bookissue.bookid,userissue.username,date,date+timedelta(days=issueDuration),0)
            db.session.add(issueEntry)
            db.session.commit()
            db.session.flush()
            data = {
                "isIssued": True,
                "id": issueEntry.id
            }
            userissue.booksissued+=1
            db.session.commit()
            if(record):
                db.session.delete(record)
                db.session.commit()
                for entry in Reserverecord.query.filter_by(bookid=bookId):
                    entry.isavailable=0
                    db.session.commit()
                    entry.returndate="NULL"
                    db.session.commit()
            return jsonify(data)
        elif(record):
            return jsonify({
                "isIssuedByAnother":False, 
                "canReserve":False
            })
        else:
            return jsonify({
                "isIssuedByAnother":False, 
                "canReserve":True
            })

@app.route('/return/<int:id>')
def returnBook(id):
    record=Issuerecord.query.filter_by(id=id).first()
    record.returned=1
    db.session.commit()
    bookid=record.bookid
    username=record.issuedto
    book=Book.query.filter_by(bookid=bookid).first()
    user=User.query.filter_by(username=username).first()
    user.booksissued-=1
    db.session.commit()
    date=datetime.now()
    record.returndate=date
    db.session.commit()
    
    flag=0
    for entry in Reserverecord.query.filter_by(bookid=bookid):
        flag=1
        entry.returndate=date
        db.session.commit()
        entry.isavailable=1
        db.session.commit()
    if(flag==0):
        book.no_of_copies+=1
        db.session.commit()


    penalty=record.penalty()
    if(penalty==0):
        return jsonify({"returned":True,"isOverdue":False})
    else:
        return jsonify({"isOverdue":True,"penalty":penalty})

@app.route('/registerBook', methods=['GET','POST'])
def registerBook():
    booknumber=(Book.query.order_by(Book.booknumber.desc()).first()).booknumber+1
    bookid=(Book.query.order_by(Book.bookid.desc()).first()).bookid+1
    # print(bookid)
    # print(booknumber)
    isbn=request.json["isbn"]
    author=request.json["author"]
    published_date=request.json["published_date"]
    title=request.json["title"]
    image_url=request.json["image_url"]
    small_image_url=request.json["small_image_url"]
    no_of_copies=request.json["no_of_copies"]
    racknumber=random.randint(1,200)
    book=Book(booknumber,bookid,isbn,author,published_date,title,image_url,small_image_url,no_of_copies,racknumber)
    # print(book.bookid)
    isbn_exists = Book.query.filter_by(isbn=isbn).first()
    bookid_exists = Book.query.filter_by(bookid=bookid).first()
    title_exists = Book.query.filter_by(title=title.strip()).first()

    exists = isbn_exists or bookid_exists or title_exists
    print(exists)
    if exists:
        data = {
            "accepted": False,
            "isbnExists": True if isbn_exists else False,
            "bookidExists": True if bookid_exists else False,
            "titleExists": True if title_exists else False ,    
        }
        return jsonify(data)

    else:
        db.session.add(book)
        db.session.commit()
        data = {
            "accepted": True,
            "isbnExists": False,
            "bookidExists": False,
            "titleExists": False,  
        }
        return jsonify(data)

@app.route("/deleteBook/<int:bookid>", methods=["DELETE"])
def bookdelete(bookid):
    book=Book.query.filter_by(bookid=bookid).first()
    print(book.title)
    book.isDeleted=1
    db.session.commit()
    return jsonify({"bookDeleted":True})


@app.route('/getExpiredBooks',methods=["GET"])
def expiredBooks():
    books=[]
    flag=0
    date=datetime.now()
    records=db.session.query(Issuerecord.bookid).distinct().all()
    for record in records:
        bookid=record.bookid
        flag=1
        issue=Issuerecord.query.filter_by(bookid=bookid).order_by(desc(Issuerecord.issuedate)).first()
        book=Book.query.filter_by(bookid=bookid).first()
        if ((int((date-datetime.strptime(issue.issuedate,'%Y-%m-%d %H:%M:%S.%f')).total_seconds())>5*365) and book):
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
                "racknumber":book.racknumber,
                "isDeleted":book.isDeleted
            })
    if(flag==1):
        data={
            "booksFound":True,
            "booksExpired":books
        }
        return jsonify(data)
    else:
        return jsonify({"booksFound":False})


if __name__=='__main__':
    app.run(debug=True)




