""" This is the main NAGBOT file where it will call the functions we write
    all your work should be done in your assigned function file and not here
    you don't need to understand this file - all you need to understand is 
    what your function needs to do. 
    
    I (Hilton) will help you connect your function to the main app - again
    all you need to worry about is your own function.
"""

'''
        Reads from the RTM Websocket stream then calls `self.process_changes(item)` for each line
        in the returned data.
        Multiple events may be returned, always returns a list [], which is empty if there are no
        incoming messages.
        :Args:
            None
        :Returns:
            data (json) - The server response. For example::
                [{u'presence': u'active', u'type': u'presence_change', u'user': u'UABC1234'}]
        :Raises:
            SlackNotConnected if self.server is not defined.
        '''
    
import os
import sqlite3
import random
import sys
import time
import re
import logging
from generate_random import generate_random
# import team member functions
from qanda import QandA # john
# from qanda import qanda # john
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

# QandA - Variables
slackBotToken = os.getenv('NAGBOT_SLACK_BOT_TOKEN', None)
slackChannel = os.getenv('NAGBOT_SLACK_CHANNEL', None)
# Variables required by qanda function.
nagbotUserId = os.getenv('NAGBOT_USER_ID', None) #slack nagbot as a user uid.
slackClient = SlackClient(slackBotToken)
userId = os.getenv('NAGBOT_TARGET_USER_ID', None) 
adminId = os.getenv('NAGBOT_ADMIN_ID', '<@U9JC2HE7R>')
question = "Have you just logged in from IP ADDRESS in LOCATION ? yes or no"
responseTime = 30 # assigned time for user to respond in seconds.
print ("1. slackBotToken is {}".format(slackBotToken))
print ("2. slackChannel is {}".format(slackChannel))
print ("3. slackClient is {}".format(slackClient))
print ("4. nagbotUserId is {}".format(nagbotUserId))
print ("5. userId is {}".format(userId))
print ("6. adminId is {}".format(adminId))

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
    # qanda(name, question, slack_client, slack_channel, nagbot_user_id, admin, resp_time)
    # qanda(userId, question, slackClient, slackChannel, nagbotUserId, adminId, responseTime)
    q = QandA(userId, question, slackClient, slackChannel, nagbotUserId, adminId, responseTime)
    q.qanda()
    forward_message = "running qanda..."
    return render_template('index.html', message=forward_message);

# Test Code Entry Point
@app.route('/api/json/z/', methods = ['POST'])
def api_json_z():
    # Create ReAlert Object
    rxjs = ReAlert()
    # Get Data being Sent
    rxjsData = rxjs.receiveJSON(request)
    # Write this Data to File
    rxjs.writeJSONToFile(request.json)
    #return rxjs.receiveJSON(request)
    return rxjsData

# Test Code Entry Point
@app.route('/api/json/nagbot/', methods = ['POST'])
def api_json_nagbot():
    # Create ReAlert Object
    rxjs = ReAlert()
    # Get Data being Sent
    rxjsData = rxjs.receiveJSON(request)
    # Write this Data to File
    rxjs.writeJSONToFile(request.json)
    #return rxjs.receiveJSON(request)
    return rxjsData
    
if __name__ == "__main__":
    # Lets make sure we only run this once.
    # Get PID of Application
    pid = str(os.getpid())
    # Location of PID File
    pidfile = "/home/ec2-user/nagbot.pid"
    
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
        