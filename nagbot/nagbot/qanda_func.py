#!/usr/bin/env python

import os
import time
import re

from slackclient import SlackClient

SLACK_BOT_TOKEN='xoxb-346474841542-DvCJe7SK4SzpRM7iEwtbhrLN'
# instantiate Slack client
slack_client = SlackClient(SLACK_BOT_TOKEN)
name="<@U9JC2HE7R>"
#admin="<@U9JC2HE7R>" #john

admin="<@U029D6F2A>" #hilton
question = "Do you like brussel sprouts ? yes or no"

        
def qanda(name, question):
    # This function takes two arguments a name and a question. It interacts with the user on a terminal command line.
    # It addresses the user by name and asks the passed question. It returns the answer which is printed to the terminal.  
    if slack_client.rtm_connect():
        print("John Bot connected and running!")
        response = "Hi," + name + "\n"+ question
        slack_client.api_call("chat.postMessage", channel="CA69A9U8J", text=response, as_user=True)
        while True:
            new_evts = slack_client.rtm_read()
            for evt in new_evts:
                if "type" in evt:
                    if evt['type']=="message" and evt['channel']=="CA69A9U8J":
                        if evt['user'] != "UA6DYQRFY" and "<@UA6DYQRFY>" not in evt['text']:
                            user_info=slack_client.api_call("users.info", user=evt['user'])
                            print(evt['text'])
                            answer=evt['text']
                            response = response_option(answer)
                            slack_client.api_call("chat.postMessage", channel=evt['channel'], text=response, as_user=True)
    else:
        print "Connection Failed, invalid token?"
        
def response_option(answer):
    if answer.lower() == "no":
        escalate(admin, name)
    else:
        reply = "Great carry on !"
    return reply

def escalate(admin, name):
    reply = " This is a test, Houston we have a problem with" + name + " login thanks John"
    qanda(admin, reply)

        
if __name__ == "__main__":
        qanda(name, question)

