from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, request
import pymongo
import bson 
import json
import jsonpickle

from flask import Flask, session
from flask import Flask,session
from datetime import timedelta
import os
import config
app = Flask(__name__)

uri = (
    "mongodb+srv://Client:PY@database.s3xgmax.mongodb.net/?retryWrites=true&w=majority"
)

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))

def get(asd):

    db = client["Auth"]
    mycol = db["Data"]
    myquery = {"email": asd}

    mydoc = mycol.find(myquery)
    
    sentdata = "lolno"
    for x in mydoc:
      sentdata = x
    lastdata = str(sentdata) # Key to check for in the BSON document
    key_to_check = 'password'
    print(lastdata)
    # Check if the key exists in the BSON document
    if key_to_check in sentdata:
        print(f"The key '{key_to_check}' exists in the BSON document with the value '{sentdata[key_to_check]}'.")
        return jsonpickle.encode(lastdata)
    else:
        print(f"The key '{key_to_check}' does not exist in the BSON document.")
        return "0"

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
    
    """ start api server """
    app.secret_key = 'why would I tell you my secret key?'
 
    
    @app.route('/session', methods=['GET', 'POST']) 
    def asd():
      if request.method == 'POST':
        #設置session
        session['username'] = 'trust'
        session.permanent = True # 长期有效，一个月的时间有效
        return "done"
      else:
        return "<form method='post' action='/session'><input type='text' name='username' />" \
              "</br>" \
              "<button type='submit'>Submit</button></form>"
    @app.route('/add', methods=['GET', 'POST']) 
    def hi():
     if request.method == 'POST': 
       db = client["Auth"]
       mycol = db["Data"]
       mydict = { "email": request.values['email'], "password": request.values['password'] }
       mycol.insert_one(mydict)
       return "done"
     return "<form method='post' action='/add'><input type='text' name='email' /><input type='text' name='password' />" \
            "</br>" \
           "<button type='submit'>Submit</button></form>"
     
    @app.route('/get', methods=['GET', 'POST']) 
    def hello():
     if request.method == 'POST': 
       return get(request.values['email'])
     return "<form method='post' action='/get'><input type='text' name='email' />" \
            "</br>" \
           "<button type='submit'>Submit</button></form>"

    if __name__ == "__main__":
        app.run(debug=True)

except Exception as e:
    print(e)
