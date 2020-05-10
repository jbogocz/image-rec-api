from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import requests
import subprocess
import json
import bcrypt
# import numpy as np
import tensorflow as tf

# Instantiate Flask api
app = Flask(__name__)
api = Api(app)

# Connect to the MongoDB client with default port
client = MongoClient('mongodb://db:27017')

# Create new database
db = client.ImageRecognition
users = db['Users']

# Check if user exists in database
def UserExist(username):
    # Find query username in MongoDB
    if users.find({'Username': username}).count() == 0:
        return False
    else:
        return True

# Register new user, inherit class from Resource
class Register(Resource):
    # define POST
    def post(self):
        # json from POST
        postedData = request.get_json()
        # get username & pass
        username = postedData['username']
        password = postedData['password']
        # Check if user already exists
        if UserExist(username):
            # if True set 301 status
            retJson = {
                'status': 301,
                'msg': 'Invalid Username'
            }
            return jsonify(retJson)

        # otherwise, if user not exists than get & hash password
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        # store user hashed password in database
        users.insert({
            'Username': username,
            'Password': hashed_pw,
            # add tokens for API
            'Tokens': 5
        })
        # return json to the user
        retJson = {
            'status': 200,
            'msg': 'You successfully signed up for this API'
        }
        return jsonify(retJson)

# Verify user hashed password
def verify_pw(username, password):
    # Check if user exists
    if not UserExist(username):
        return False
    # get hashed pass
    hashed_pw = users.find({
        'Username': username
    })[0]['Password']
    # match hashed passwords user provide vs stored in mongodb
    if bcrypt.hashpw(password.endcode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

