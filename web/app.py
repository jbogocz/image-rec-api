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
    if users.find({'Username':username}).count()==0
        return False
    else:
        return True

