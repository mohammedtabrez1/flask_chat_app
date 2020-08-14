import json

from flask import (Flask, after_this_request, flash, jsonify, redirect,
                   render_template, request, session, url_for)
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from flask_socketio import SocketIO
from pymongo.errors import DuplicateKeyError
from werkzeug.exceptions import BadRequestKeyError

from config import Config
from mongodb import get_all_messages, get_user, save_message, save_user

app = Flask(__name__)
app.secret_key=Config.SECRET_KEY
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.login_view='login'
login_manager.init_app(app)

msgs = []

NAME_KEY='name'
@app.route("/signup")
@app.route("/", methods=['POST','GET'])
def signup():
    """
    :return: return the signup page and handles all the authentication scenarios
    """
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
    """
    :return: returns login page and handles authentication scenarios
    """
    if current_user.is_authenticated:
        return redirect(url_for('chat_room'))
    message = ''
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user(username)
        if username and password:
            if user and user.check_password(password):
                login_user(user)
                session[NAME_KEY] = username
                flash(f'You were successfully logged in as {username}.')
                return redirect(url_for('chat_room'))
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
        try:
            message=request.args['message']
            return render_template('login.html',message=message)
        except BadRequestKeyError:
            return render_template('login.html')


@app.route("/chat_room",methods=['GET','POST'])
def chat_room():
    """
    :return: returns chat_room page if the user is authhenticated
    """
    if current_user.is_authenticated:
        return render_template('chat_room.html')
    else:
         return redirect(url_for('login'))


@app.route("/logout")
def logout():
    """
    Logs the user out from the session
    :return: None
    """
    session.pop(NAME_KEY,None)
    logout_user()
    return render_template('logout.html')

@socketio.on('send_message')
def broadcast_message(data):
    """
    :param data: reveives name and the message from the user
    :return: broadcast the message to all the other users except self
    """
    name = data['name']
    msg = data['msg']
    save_message(name,msg)
    socketio.emit('receive',{'name':name,'msg':msg},broadcast=True, include_self=False)

@app.route("/get_messages",methods=['GET','POST'])
def get_messages():
    """
    :return: a json object with the list of data from mongodb
    """
    return jsonify({'data':(get_all_messages())})



@app.route("/get_name",methods=['GET','POST'])
def get_name():
    """
    :return: a json object storing name of logged in user
    """
    data = {"name": ""}
    if 'name' in session:
        data = {"name": session['name']}
    return jsonify(data)


@login_manager.user_loader
def load_user(username):
    return get_user(username)



if __name__=="__main__":
    socketio.run(app, debug=Config.FLASK_DEBUG)
