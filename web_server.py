from crawl import *
from redis import StrictRedis
from flask import Flask
import time

redis = StrictRedis(password="2921038")

app = Flask(__name__)

@app.route("/")
def hello_world():

    with open("time.txt","r") as file:
        a = file.read()
    return a
