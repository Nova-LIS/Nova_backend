from app import db

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
