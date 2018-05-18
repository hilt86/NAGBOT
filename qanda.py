import time
import logging


# create logger
# module_logger = logging.getLogger('nagbot.realert.qanda')

logger = logging.getLogger('nagbot.qanda')
logger.info('qanda')


def qanda(user_id, ip_add, timestamp):
    """
    This function sends and retrieves responses from Slack as nagbot to assigned users.
    name is the name of the target user.
    question the queestion requireing a yes or no answer.
    slack_client is the OAuth token reuired to communicate with Slack
    slack_channel and nagbot_user are the channel and bot user id's.
    resp_time defines how long in sec a user has to respond befor admin is notified.
    """
    name="<@"+user_id+">"
    question="Hi" + name + "\n At " + timestamp + " Have you just logged in from "+ip_add+" ? "
    return question

def escalate(user_id, ip_add, slack_client, escalate_channel):
    logger.warning("Escalation Detected !")
    # This function defines what to do in the case of a negative response from a user. ie notify admin.
    name="<@"+user_id+">"
    reply =  " This is a test, " + name + "s login from "+ip_add+" requires attention !!!"
    slack_client.api_call("chat.postMessage", channel=escalate_channel, text=reply, as_user=True)
    return
    
