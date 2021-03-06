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

# Generate return dictionary for user
def generateReturnDictionary(status, msg):
    retJson = {
        'status': status,
        'msg': msg
    }
    return retJson

# Check user credentials
def verifyCredentials(username, password):
    # Check if user exists
    if not UserExist(username):
        return generateReturnDictionary(301, 'Invalid Username'), True
    # Check if password is valid
    correct_pw = verify_pw(username, password)
    if not correct_pw:
        return generateReturnDictionary(302, 'Invalid Password'), True

    return None, False

# Recognize provided image and return answer to the user
class Classify(Resource):
    # json from POST
    def post(self):
        postedData = request.get_json()
        # get username, pass & image url
        username = postedData['username']
        password = postedData['password']
        ur = postedData['url']

        # verify credentials from user
        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        # check if user has enough tokens
        tokens = user.find({
            'Username': username
        })[0]['Tokens']

        if tokens <= 0:
            return jsonify(generateReturnDictionary(303, 'Not Enough Tokens!'))

        # get content of url
        r = requests.get(url)
        # create empty dictionary
        retJson = {}
        # write url content to the temporary file
        with open('temp.jpg', 'wb') as f:
            f.write(r.content)
            # open new subprocess with tensorflow file & pass args
            proc = subprocess.Popen(
                'python classify_image.py --model_dir=. --image_file=./temp.jpg')
            proc.communicate()[0]
            proc.wait()
            # load dictionary which was stored in text.txt
            with open('text.txt') as g:
                retJson = json.load(g)
        # Substract one token from user
        users.update({
            'Username': username
        }, {
            '$set': {
                'Tokens': tokens-1
            }
        })
        # Return response to the user
        return retJson

# Refill tokens for user
class Refill(Resource):
    # json from POST
    def post(self):
        postedData = request.get_json()

        username = postedData['username']
        password = postedData['admin_pw']
        amount = postedData['amount']

        # Check if admin exists
        if not UserExist(username):
            return jsonify(generateReturnDictionary(301, 'Invalid Username'))
        # Check if admin pass is correct
        correct_pw = 'admin1'  # just for now, should be hashed and stored in DB
        if not password == correct_pw:
            return jsonify(
                generateReturnDictionary(304, 'Invalid Administrator Password'))
        # refill user tokens
        users.update({
            'Username': username
        }, {
            '$set': {
                'Tokens': amount
            }
        })
        return jsonify(generateReturnDictionary(200, 'Refilled Successfully'))


# add resources to the API
api.add_resource(Register, '/register')
api.add_resource(Classify, '/classify')
api.add_resource(Refill, '/refill')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
