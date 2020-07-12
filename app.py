from flask import Flask,render_template,request,redirect,url_for,session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import Config
from mongodb import save_user,get_user
from pymongo.errors import DuplicateKeyError
from user import User
import json

app=Flask(__name__)
app.secret_key=Config.SECRET_KEY
login_manager = LoginManager()
login_manager.login_view='login'
login_manager.init_app(app)

@app.route("/signup", methods=['POST','GET'])
def signup():
    message = ''
    if request.method=='POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if username and email and password:
            try:
                save_user(username,email,password)
                message = json.dumps("you have signed up successfully, please login")
                session[message]=message
                return redirect(url_for('login',message=message))
            except DuplicateKeyError:
                message='This username is already present in database, please try with different user'
                return render_template('signup.html',message=message)
        else:
            message = 'user is not created, please fill the form before submitting'
            return render_template('signup.html', message=message)
    else:
        return render_template('signup.html')


@app.route("/login", methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    message = ''
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user(username)
        if username and password:
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('home'))
            elif not user:
                message= f'{username} is not registered, please signup'
                session[message]=message
                return render_template('login.html', message=message)
            elif not user.check_password(password):
                message = f'Wrong password, please enter the correct password to login'
                return render_template('login.html', message=message)
        elif username and not password:
            message = 'please enter password before submitting'
            return render_template('login.html', message=message)

        else:
            message = 'please enter username and password before submitting'
            return render_template('login.html', message=message)
    else:
        message=request.args['message']
        return render_template('login.html',message=json.loads(message))


@app.route("/home")
def home():
    if current_user.is_authenticated:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    logout_user()
    return render_template('logout.html')

@login_manager.user_loader
def load_user(username):
    return get_user(username)

if __name__=="__main__":
    app.run(Config.FLASK_DEBUG)

