from flask import Flask,render_template,request,redirect,url_for,session,jsonify,flash,after_this_request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO
from mongodb import save_user,get_user,save_message,get_all_messages
from pymongo.errors import DuplicateKeyError
from werkzeug.exceptions import BadRequestKeyError
import json
from config import Config





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
    print(f'get_messgae:  {get_all_messages()}')
    app.logger.info(f'name : {name}  -  msg : {msg}')

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

    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    data = {"name": ""}
    if 'name' in session:
        data = {"name": session['name']}
    app.logger.info(f'data:{data}')
    return jsonify(data)


@login_manager.user_loader
def load_user(username):
    return get_user(username)



if __name__=="__main__":
    socketio.run(app, debug=Config.FLASK_DEBUG, host='0.0.0.0',port='5000')

