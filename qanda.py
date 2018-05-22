import time
import os
from slackclient import SlackClient
import logging
import threading
from threading import Timer

# create logger
# module_logger = logging.getLogger('nagbot.realert.qanda')

SLACK_BOT_TOKEN =  os.environ["NAGBOT_SLACK_BOT_TOKEN"]
slack_client = SlackClient(SLACK_BOT_TOKEN)
test_attachments_json = [
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

logger = logging.getLogger('nagbot.qanda')
logger.info('qanda')

def qanda(user_id, ip_add):
    """
    This function sends and retrieves responses from Slack as nagbot to assigned users.
    name is the name of the target user.
    question the queestion requireing a yes or no answer.
    slack_client is the OAuth token reuired to communicate with Slack
    slack_channel and nagbot_user are the channel and bot user id's.
    resp_time defines how long in sec a user has to respond befor admin is notified.
    """
    logger.debug("qanda.test received : " + user_id + " and " + ip_add)
    slack_client.api_call(
    "chat.postMessage",
    channel=user_id,
    text=("Hey " + user_id + " did you just login from " + ip_add + " ?"),
    attachments=test_attachments_json
    )
    

def escalate(user_id, ip_add, slack_client, escalate_channel):
    # print("### Escalate ran ###")
    logger.warning("Escalation Detected !")
    # This function defines what to do in the case of a negative response from a user. ie notify admin.
    name="<@"+user_id+">"
    reply =  "SECURITY ALERT : " + "There has been a suspicious login using " + name + "'s " + "credential"
    slack_client.api_call("chat.postMessage", channel=escalate_channel, text=reply, as_user=True)
    return

