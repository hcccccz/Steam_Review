# from crawl import *
from redis import StrictRedis
from flask import Flask,render_template
import time
import json

redis = StrictRedis(password="2921038")

app = Flask(__name__)

@app.route("/")
def hello_world():

    with open("log.json","r") as file:
        log = json.loads(file.read())
        fail = log["Fail"]
        spy_status= log['spy_status']
        success = log['Success']
        requested = redis.dbsize()
        total = log['Total']
        fail_rate = str(round(fail/requested *100,3)) + "%"
        percent = str(round(requested/total *100,3)) + "%"
    return render_template("index.html",spy_status=spy_status,fail=fail,success=success,fail_rate=fail_rate,requested=requested,percent=percent)
