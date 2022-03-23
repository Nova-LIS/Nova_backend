from flask import Flask,render_template,flash,url_for,redirect,request,jsonify
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_marshmallow import Marshmallow
# from forms import RegistrationForm,LoginForm
from flask_cors import CORS

db=SQLAlchemy()
# migrate = Migrate()
# ma = Marshmallow()
cors = CORS()
app = Flask(__name__)
app.config['SECRET_KEY']='0099734a1b530d8a8de2f3b7d091b60c'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db.init_app(app)

class User(db.Model):
    name = db.Column(db.String(50),nullable=False,unique=True)
    roll = db.Column(db.String(10), nullable=False, unique=True)
    email=db.Column(db.String(100),unique=True,nullable=False)
    phone=db.Column(db.String(10),unique=True,nullable=False)
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
# @app.route('/hello',methods=['GET','POST'])
def about():
    return render_template('./about.html',title='About')


@app.route('/register',methods=['GET','POST'])
def register():
    print("Reached")
    input_json = request.get_json(force=True)
    dictToReturn = {'name':input_json['name'],'roll': input_json['roll'],'email': input_json['email'],'phone': input_json['phone'],'username': input_json['userName'],'password': input_json['password']}

    record = User(dictToReturn['name'],dictToReturn['roll'],dictToReturn['email'],dictToReturn['phone'],dictToReturn['username'],dictToReturn['password'])
    db.session.add(record)
    db.session.commit()
    return jsonify(dictToReturn)
    # return render_template('./register.html', title='About')

# @app.route('/hello',methods=['GET','POST'])
# def hello():
#     print("reached")
#     return render_template('./about.html', title='About')

    # form = RegistrationForm()
    # if form.validate_on_submit():
    #     flash(f'Account created for {form.username.data}!', 'success')
    #     return redirect(url_for('home'))

    # input_json = request.get_json(force=True)
    # dictToReturn = {'name':input_json['name'],'roll': input_json['roll'],'email': input_json['email'],'phone': input_json['phone'],'username': input_json['userName'],'password': input_json['password']}
    #
    # record = User(dictToReturn['name'],dictToReturn['roll'],dictToReturn['email'],dictToReturn['phone'],dictToReturn['username'],dictToReturn['password'])
    # db.session.add(record)
    # db.session.commit()
    # return jsonify(dictToReturn)
    # #return 'This is my first API call!'
    #     #print(dictToReturn['text'])
    # #print(dictToReturn['id'])
    # #record = User("1", form.name.data, form.roll.data, form.email.data, form.username.data, "reg.jpg", 50,
    #               #form.password.data)
    # #     db.session.add(record)
    # #     db.session.commit()
    # form=RegistrationForm()
    # if form.validate_on_submit():
    #     print(form.password.data)
    #     flash(f'Account created for {form.username.data} !','success')
    #     record = User("1",form.name.data,form.roll.data,form.email.data,form.username.data,"reg.jpg",50,form.password.data)
    #     db.session.add(record)
    #     db.session.commit()
    #     return redirect(url_for('home'))
    # return render_template('register.html',title='Register',form=form)


# @app.route('/login',methods=['GET','POST'])
# def login():
#     form=LoginForm()
#     if form.validate_on_submit():
#         flash(f'Successfully Logged In!','success')
#         return redirect(url_for('home'))
#     return render_template('login.html',title='Login',form=form)


if __name__=='__main__':
    app.run(debug=True)
    # migrate.init_app(app, db)
    # ma.init_app(app)
    cors.init_app(app)





