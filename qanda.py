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
    admin_user="<@"+admin+">"
    question="Hi" + name + "\n At " + timestamp + " Have you just logged in from "+ip_add+" ? "
    return question
   
        
def askQuestion(name, question, slack_client, slack_channel, nagbot_user_id, admin, resp_time):
    if slack_client.rtm_connect():
        response = name + question
    else:
        # print "Connection Failed, invalid token?"
        logger.warning("Connection Failed, invalid token?")
    return

def grabResponses(name, slack_client, slack_channel, nagbot_user_id ):
    if slack_client.rtm_connect():
        slack_client.api_call("chat.postMessage", channel=slack_channel, text="Hello from Python! :tada:",
        user=name)
        # print "got here"
        logger.debug("got here")
    else:
        logger.warning("Connection Failed, invalid token?")
        # print "Connection Failed, invalid token?"


def escalate(name, slack_client, ip_add):
    logger.warning("Escalation Detected !")
    # This function defines what to do in the case of a negative response from a user. ie notify admin.
    reply =  " This is a test, " + name + "s login from "+ip_add+" requires attention !!!"
    slack_client.api_call("chat.postMessage", channel="CARFQNLQN", text=reply, as_user=True)
    reply=" "
    return reply
    
def time_out(name, slack_client, ip_add):
    # This function defines what to do if the user does not respond iin the allocated time.
    reply = " User " + name + " has not replied to login from " +ip_add+" alert in acceptable timeframe"
    slack_client.api_call("chat.postMessage", channel="CARFQNLQN", text=reply, as_user=True)
    return
