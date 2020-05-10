from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import requests
import subprocess
import json
import bcrypt
# import numpy as np
import tensorflow as tf

app = Flask(__name__)
api = Api(app)

