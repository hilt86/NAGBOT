# all the imports
import os
import sqlite3
import random
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
    
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
    return  "Hello team!" + " here is a random integer : " + str(random.randint(1,101))
