""" This is the main NAGBOT file where it will call the functions we write
    all your work should be done in your assigned function file and not here
    you don't need to understand this file - all you need to understand is
    what your function needs to do.

    I (Hilton) will help you connect your function to the main app - again
    all you need to worry about is your own function.
"""
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, json, Response, jsonify, make_response
import os
import json
import sys
import time
# import threading
# from threading import *
import re
import logging
# from qanda import * 
from qanda import qanda, escalate
from realert import ReAlert
import celery
# import pprint

from slackclient import SlackClient

if os.environ.get('DEBUG'):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('nagbot')
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# Create Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# create console handler and set level to debug
console = logging.StreamHandler()
# This will take anything from DEBUG and Up
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(console)

# Your app's Slack bot user token
SLACK_BOT_TOKEN =  os.environ["NAGBOT_SLACK_BOT_TOKEN"]
SLACK_VERIFICATION_TOKEN = os.environ["NAGBOT_SLACK_VERIFICATION_TOKEN"]
slack_channel=os.environ["NAGBOT_SLACK_CHANNEL"]

user_id= os.environ["NAGBOT_USER_ID"]
escalate_channel=os.environ["NAGBOT_SLACK_ESCALATE_CHANNEL"]

# Global Test Variables
ip_add="1.1.1.1"
timeout_secs=30


# Slack client for Web API requests
slack_client = SlackClient(SLACK_BOT_TOKEN)

# Flask webserver for incoming traffic from Slack
app = Flask(__name__)
BROKER_URL=os.environ['REDIS_URL']
CELERY_RESULT_BACKEND=os.environ['REDIS_URL']


celery_i = celery.Celery('example')

@celery_i.task
def my_background_task(arg1, arg2):
    # some long running task here
    print(" ### I am a background task ### ")
    return "background task finished"
        

# Helper for verifying that requests came from Slack
def verify_slack_token(request_token):
    if SLACK_VERIFICATION_TOKEN != request_token:
        logger.warning("Error: invalid verification token!")
        logger.warning("Received {} but was expecting {}".format(request_token, SLACK_VERIFICATION_TOKEN))
        return make_response("Request contains invalid Slack verification token", 403)

@app.route('/')
def run_background():
    print(" ### background app route ### ")
    my_background_task.delay(10, 20)
    return 'gotcha'


# Test Code Entry Point
@app.route('/api/json/nagbot/', methods = ['POST'])
def api_json_nagbot():
    # Create ReAlert Object
    rxjs = ReAlert()
    # Get Data being Sent
    rxjsData = rxjs.receiveJSON(request)
    # print(rxjsData)
    # Write this Data to File
    if rxjsData:
        ip_add, user_id, timeStamp = rxjsData
        logger.debug("IP Address: {0} User Id: {1} timeStamp: {2}".format(ip_add, user_id, timeStamp))
        # qanda(user_id, ip_add, slack_client, slack_channel, nagbot_user_id, admin, resp_time, timeStamp)
        qanda(user_id, ip_add)
        # rxjs.writeJSONToFile(request.json)
        # message_actions()
        return make_response("JSON OK", 200)
    else:
        return make_response("JSON BAD", 400)


# The endpoint Slack will load your menu options from
@app.route("/slack/message_options", methods=["POST"])
def message_options():
    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    # Verify that the request came from Slack
    verify_slack_token(form_json["token"])

    # Dictionary of menu options which will be sent as JSON
    menu_options = {
        "options": [
            {
                "text": "Wasn't me",
                "value": "no"
            },
            {
                "text": "That was me",
                "value": "yes"
            }
        ]
    }

    # Load options dict as JSON and respond to Slack
    return Response(json.dumps(menu_options), mimetype='application/json')


# The endpoint Slack will send the user's menu selection to
@app.route("/slack/message_actions", methods=["POST"])
def message_actions():

    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    # Verify that the request came from Slack
    verify_slack_token(form_json["token"])

    # Check to see what the user's selection was and update the message accordingly
    selection = form_json["actions"][0]["selected_options"][0]["value"]    
    response_user = form_json["user"]["id"]   
    if selection == "no":
        message_text = "ok, alerting secops"
        escalate(response_user, ip_add, slack_client, escalate_channel)
    elif selection == "yes":
        message_text = "sorry to bother you!"
    else:
        message_text = "something is wrong"

    slack_client.api_call(
      "chat.update",
      channel=form_json["channel"]["id"],
      ts=form_json["message_ts"],
      text="{}".format(message_text),
      attachments=[] # empty `attachments` to clear the existing massage attachments
    )

    # Send an HTTP 200 response with empty body so Slack knows we're done here
    return make_response("", 200)

# Send a Slack message on load. This needs to be _before_ the Flask server is started

# A Dictionary of message attachment options
attachments_json = [
    {
        "fallback": "Upgrade your Slack client to use messages like these.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "callback_id": "menu_options_2319",
        "actions": [
            {
                "name": "response_list",
                "text": "choose your response...",
                "type": "select",
                "data_source": "external"
            }
        ]
    }
]

# Start the Flask server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
