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
from qanda import qanda, response_option, escalate # john
from createrules import createrules # bandr
from realert import realert # dustin
# flask modules
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
# slack modules
from slackclient import SlackClient

SLACK_BOT_TOKEN='xoxb-346474841542-DvCJe7SK4SzpRM7iEwtbhrLN'
# instantiate Slack client
slack_client = SlackClient(SLACK_BOT_TOKEN)
name="<@U9JC2HE7R>"
#admin="<@U9JC2HE7R>" #john
#admin="<@U9HEUKN7P>" #dustin
#admin="<@U9V7C7W31>" #bandr
admin="<@U029D6F2A>" #hilton
question = "Do you like brussel sprouts ? yes or no"
    
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
    qanda(name, question, slack_client)
    forward_message = "running qanda..."
    return render_template('index.html', message=forward_message);

