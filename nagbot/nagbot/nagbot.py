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
from qanda import * # john
from createrules import createrules # bandr
#from realert import realert # dustin
from realert import ReAlert # dustin
# flask modules
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, json, Response, jsonify
# slack modules
from slackclient import SlackClient
# For Debuggintg TimeStamps
# Remove in Prod
from datetime import datetime
# import datetime
from datetime import date

def addYears(d, years):
    try:
#Return same day of the current year        
        return d.replace(year = d.year + years)
    except ValueError:
#If not same day, it will return other, i.e.  February 29 to March 1 etc.        
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))

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
SLACK_BOT_TOKEN = os.environ["NAGBOT_SLACK_BOT_TOKEN"]
slack_channel="CA69A9U8J" #slack nagbot_live_here channel id
nagbot_user_id="UAMJZ591D" #slack nagbot as a user uid.
# instantiate Slack client
slack_client = SlackClient(SLACK_BOT_TOKEN)

# logger.debug('SLACK_BOT_TOKEN is: {0}'.format(SLACK_BOT_TOKEN))



user_id="U9JC2HE7R" #john assigned admin user on nagbot_live_here channel.
# admin="U9HEUKN7P" #dustin
# admin="U9V7C7W31" #bandr
admin="U029D6F2A" #hilton
#question = "Have you just logged in from "+ip_add+ "? yes or no"
ip_add="12345"
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
    return render_template('index.html')

@app.route("/qanda/", methods=['POST'])
def run_qanda():
    # name, admin and slack_client are also required by escalate function. Not sure how to pass arguments from nagbot.py
    # have duplicated in qanda.py for now :john.
    qanda(user_id, ip_add, slack_client, slack_channel, nagbot_user_id, admin, resp_time)
    forward_message = "running qanda..."
    return render_template('index.html', message=forward_message);
    
@app.route("/askQuestion/", methods=['POST'])
def run_ask():
    # name, admin and slack_client are also required by escalate function. Not sure how to pass arguments from nagbot.py
    # have duplicated in qanda.py for now :john.
    askQuestion("<@U029D6F2A>", "what color are your socks?", slack_client, slack_channel, nagbot_user_id, admin, resp_time)
    forward_message = "running askQuestion..."
    return render_template('index.html', message=forward_message);
    
@app.route("/grabResponses/", methods=['POST'])
def run_grabResponses():
    respons = grabResponses("<@U029D6F2A>", slack_client, slack_channel, nagbot_user_id)
    return render_template('return.html', message=respons);

# Test Code Entry Point
@app.route('/api/json/nagbot/', methods = ['POST'])
def api_json_nagbot():
    # Create ReAlert Object
    rxjs = ReAlert()
    # Get Data being Sent
    rxjsData = rxjs.receiveJSON(request)
    # Write this Data to File
    if rxjsData:
        ip_add, user_id, timeStamp = rxjsData
        # datetimeObject = datetime.strptime(timeStamp, '%b %d %I:%M:%S') # This is for Debug - Not for Prod
        # dO = addYears(datetimeObject, 118) # This is for Debug - Not for Prod
        # logger.debug('{2}|{3} : User Id is: {0} IP Address is: {1}'.format(user_id, ip_add, timeStamp, dO)) # This is for Debug - Not for Prod
        # qanda(user_id, ip_add, slack_client, slack_channel, nagbot_user_id, admin, resp_time, timeStamp)
        rxjs.writeJSONToFile(request.json)
        return Response('OK', status=200)
        # return 'OK'
    else:
        return Response('NOT OK', status=404)



if __name__ == "__main__":
    # Lets make sure we only run this once.
    # Get PID of Application
    pid = str(os.getpid())
    # Location of File
    pidfile = "nagbot.pid"
    
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
        logger.info("{} - loop test ... ".format(pid))
        # Clean Up
        # Remove PID File
        logger.info("{0} - Remove PID File : {1}".format(pid, pidfile))
        os.unlink(pidfile)
    except pidFileExists:
        logger.error("{} - Pid File Exists!, exiting ... ".format(pid))
        sys.exit(2)
    except Exception as e:
        #except Exception as e: print(e)
        logger.warning("{0} - {1}".format(pid,e))
    finally:
        logger.info("{} - Finished".format(pid))("{} - Finished".format(pid))