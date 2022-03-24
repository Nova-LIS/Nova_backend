# from flask import current_app,request
from __main__ import app
from app import create_app,db
from flask import current_app,render_template,flash,url_for,redirect,request,jsonify
from models import Book,User

app=create_app()

@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
def home():
    return render_template('./home.html',title='Home')


@app.route('/about',methods=['GET','POST'])
def about():
    return render_template('./about.html',title='About')


@app.route('/register',methods=['GET','POST'])
def register():

    print("Entered")

    #input_json = request.get_json(force=True)
    #print(input_json)
    
    name=request.json['name']
    roll=request.json['roll']
    email=request.json['email']
    phone=int(request.json['phone'])
    username=request.json['userName']
    password=request.json['password']
    print(name)
    record = User(name,roll,email,phone,username,password)
    db.session.add(record)
    db.session.commit()
    #return render_template('./about.html', title='Register')
    return jsonify(record.serialize())
# @app.route('/',methods=['GET','POST'])
# @app.route('/home',methods=['GET','POST'])
# def home():
#     return render_template('./templates/home.html',title='Home')


# @app.route('/about',methods=['GET','POST'])
# def about():
#     return render_template('./templates/about.html',title='About')


# @app.route('/register',methods=['GET','POST'],strict_slashes=False)
# def register():
#     print("reached")
#     input_json = request.get_json(force=True)
#     dictToReturn = {'name':input_json['name'],'roll': input_json['roll'],'email': input_json['email'],'phone': input_json['phone'],'username': input_json['userName'],'password': input_json['password']}

#     record = User(dictToReturn['name'],dictToReturn['roll'],dictToReturn['email'],dictToReturn['phone'],dictToReturn['username'],dictToReturn['password'])
#     db.session.add(record)
#     db.session.commit()
#     return jsonify(dictToReturn)
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