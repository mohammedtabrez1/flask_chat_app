from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from bson import ObjectId
from user import User
import datetime


client=MongoClient("mongodb+srv://Tabrez:Tabrez@cluster.s1d75.mongodb.net/<dbname>?retryWrites=true&w=majority")
chat_db=client.get_database("AppDatabase")
users_collection= chat_db.get_collection("Users")
messages_collection= chat_db.get_collection("Messages")

def save_user(username,email,password):
    hashed_password=generate_password_hash(password)
    users_collection.insert_one({'_id':username,'email': email,'password':hashed_password,'created_on':datetime.datetime.now()})

def get_user(username):
    data=users_collection.find_one({'_id':username})
    return User(data['_id'],data['email'],data['password']) if data else None

def save_message(username,message):
    """
    :param username: takes the username from the user
    :param message: takes the message from the user
    :return: inset into mongoDB message collection
    """
    messages_collection.insert_one({'username':username,'message':message,'messaged_on':datetime.datetime.now()})

def get_all_messages():
    """
    :return: list of sorted data in reverse order
    """
    messages=messages_collection.find().sort([('messaged_on',-1)])
    return_list=[]
    for message in messages:
        return_list.append({'username':message['username'],'message':message['message']})
    return return_list[::-1]



#print({'data':(get_all_messages())})