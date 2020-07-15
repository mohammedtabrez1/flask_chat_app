from flask import Flask,render_template,request,redirect,url_for,session,jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO
from mongodb import save_user,get_user#,get_messages,get_room,get_room_members,is_room_member
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


@app.route("/", methods=['POST','GET'])
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
        return redirect(url_for('chat_room'))
    message = ''
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user(username)
        if username and password:
            if user and user.check_password(password):
                login_user(user)
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

    return render_template('chat_room.html')


@app.route("/logout")
def logout():
    logout_user()
    return render_template('logout.html')

@socketio.on('send_message')
def broadcast_message(data):
    name = data['name']
    msg = data['msg']
    #save the message to db here

    socketio.emit('receive',jsonify(data))

@app.route("/get_name")
def get_name():
    """
    :return: a json object storing name of logged in user
    """
    user=current_user
    print(user)
    return jsonify({'user':user})
'''
@app.route('/rooms/<room_id>/')
@login_required
def view_room(room_id):
    room = get_room(room_id)
    if room and is_room_member(room_id, current_user.username):
        room_members = get_room_members(room_id)
        messages = get_messages(room_id)
        return render_template('view_room.html', username=current_user.username, room=room, room_members=room_members,
                               messages=messages)
    else:
        return "Room not found", 404
'''
@login_manager.user_loader
def load_user(username):
    return get_user(username)



if __name__=="__main__":
    socketio.run(app, debug=Config.FLASK_DEBUG)
