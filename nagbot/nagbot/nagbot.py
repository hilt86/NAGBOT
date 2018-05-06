#!/bin/env python 

""" This is the main NAGBOT file where it will call the functions we write
    all your work should be done in your assigned function file and not here
    you don't need to understand this file - all you need to understand is 
    what your function needs to do. 
    
    I (Hilton) will help you connect your function to the main app - again
    all you need to worry about is your own function.
"""
    
import os
import sqlite3
import random
import sys
import time
import re
import logging
from generate_random import generate_random
# import team member functions
from qanda import qanda # john
from createrules import createrules # bandr
#from realert import realert # dustin
from realert import ReAlert # dustin
# flask modules
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, json, Response, jsonify
# slack modules
from slackclient import SlackClient

# Setup Logging
# Create logger
logger = logging.getLogger('nagbot')
logger.setLevel(logging.DEBUG)

# Create Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# create file handler which logs even debug messages
logfile = logging.FileHandler('nagbot.log')
# This will take anything from DEBUG and Up
logfile.setLevel(logging.DEBUG)
logfile.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(logfile)

# create console handler and set level to debug
console = logging.StreamHandler()
# This will take anything from DEBUG and Up
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(console)

# Variables required by qanda function.
SLACK_BOT_TOKEN='xoxb-346474841542-DvCJe7SK4SzpRM7iEwtbhrLN'
slack_channel="CA69A9U8J" #slack nagbot_live_here channel id
nagbot_user_id="UA6DYQRFY" #slack nagbot as a user uid.
# instantiate Slack client
slack_client = SlackClient(SLACK_BOT_TOKEN)
name="<@U9JC2HE7R>"  # target user id as obtained from Elastalert.
admin="<@U9JC2HE7R>" #john assigned admin user on nagbot_live_here channel.
#admin="<@U9HEUKN7P>" #dustin
#admin="<@U9V7C7W31>" #bandr
#admin="<@U029D6F2A>" #hilton
question = "Have you just logged in from IP ADDRESS in LOCATION ? yes or no"
resp_time=30 # assigned time for user to respond in seconds.

# Exception Class
class pidFileExists(Exception):
    pass

# Start Flask Application
app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path , 'nagbot.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
# setting silent to False will make the app complain if the environment
# variable is not set
app.config.from_envvar('NAGBOT_SETTINGS', silent=True)
        
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        
@app.route("/")
def hello():
    #return  "Hello team!" + " here is a random integer : "  + str(generate_random(1000))
    return render_template('index.html')

@app.route("/qanda/", methods=['POST'])
def run_qanda():
    # name, admin and slack_client are also required by escalate function. Not sure how to pass arguments from nagbot.py
    # have duplicated in qanda.py for now :john.
    qanda(name, question, slack_client, slack_channel, nagbot_user_id, admin, resp_time)
    forward_message = "running qanda..."
    return render_template('index.html', message=forward_message);

# Test Code Entry Point
@app.route('/api/json/z/', methods = ['POST'])
def api_json_z():
    rxjs = ReAlert()
    return rxjs.receiveJSON(request)

if __name__ == "__main__":
    # Lets make sure we only run this once.
    # Get PID of Application
    pid = str(os.getpid())
    # Location of File
    pidfile = "./nagbot.pid"
    
    try:
        # Check if File Exists i.e. we have something running already.
        if os.path.isfile(pidfile):
            raise pidFileExists
        else:
            # Generate PidFile
            file(pidfile, 'w').write(pid)
            logger.info("{0} - Started {1}".format(pid, "NagBOT"))
        
        # Start App
        app.run(host='0.0.0.0')
        
        # Clean Up
        # Remove PID File
        logger.info("{0} - Remove PID File : {1}".format(pid, pidfile))
        os.unlink(pidfile)
    except pidFileExists:
        logger.info("{} - Pid File Exists!, exiting ... ".format(pid))
        sys.exit(2)
    except:
        logger.info("{} - Something Broke".format(pid))
    finally:
        logger.info("{} - Finished".format(pid))
        