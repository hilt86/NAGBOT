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
from generate_random import generate_random
# import team member functions
from qanda import qanda # john
from createrules import createrules # bandr
from realert import realert # dustin
# flask modules
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
# slack modules
from slackclient import SlackClient

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
question = "Do you like single malt highland whiskey ? yes or no"
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
#print ("App Root Path is : {}".format(app.root_path))
#app.run()
        
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
        # Start App
        app.run(host='0.0.0.0')
        
        # Clean Up
        # Remove PID File
        print("Remove PID File ({0}): {1}".format(pid, pidfile))
        os.unlink(pidfile)
    except pidFileExists:
        print ("Pid File Exists !!!")
        sys.exit(2)
    except:
        print("Something Broke")
    finally:
        # Remove PID File
        print("NAGBOT Finished !!!!!")
        #os.unlink(pidfile)