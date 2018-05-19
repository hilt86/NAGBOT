import time
import logging
import threading
from threading import Timer

# create logger
# module_logger = logging.getLogger('nagbot.realert.qanda')

logger = logging.getLogger('nagbot.qanda')
logger.info('qanda')

def test(user_id, ip_add):
    logger.debug("qanda.test received : " + user_id + " and " + ip_add)


def qanda(user_id, ip_add, timestamp):
    """
    This function sends and retrieves responses from Slack as nagbot to assigned users.
    name is the name of the target user.
    question the queestion requireing a yes or no answer.
    slack_client is the OAuth token reuired to communicate with Slack
    slack_channel and nagbot_user are the channel and bot user id's.
    resp_time defines how long in sec a user has to respond befor admin is notified.
    """
    # print("### Qanda ran ###")
    logger.debug("Qanda Running")
    name="<@"+user_id+">"
    question="Hi" + name + "\n At " + timestamp + " Have you just logged in from "+ip_add+" ? "
    return question

def escalate(user_id, ip_add, slack_client, escalate_channel):
    # print("### Escalate ran ###")
    logger.warning("Escalation Detected !")
    # This function defines what to do in the case of a negative response from a user. ie notify admin.
    name="<@"+user_id+">"
    reply =  " This is a test, " + name + "s login from "+ip_add+" requires attention !!!"
    slack_client.api_call("chat.postMessage", channel=escalate_channel, text=reply, as_user=True)
    return

def response_timer(secs,user_id, ip_add, slack_client, escalate_channel):
# If timer is exceeded escalate to secops
    t=threading.Timer(secs,time_out(user_id, ip_add, slack_client, escalate_channel))
    # Start the timer
    t.start()
    return
        
# If user responds stop the timer  
def stopper():
    # t.cancel()
    #  print "stopped"
    logger.info("Timer stopped")
    return
    
def time_out(user_id, ip_add, slack_client, escalate_channel):
    # print("### Time out ran ###")    
    logger.warning("Timeout Detected !")
    # This function defines what to do in the case of a negative response from a user. ie notify admin.
    name="<@"+user_id+">"
    reply =  " This is a test, " + name + "s login from "+ip_add+" has not responded in required time interval!!!"
    slack_client.api_call("chat.postMessage", channel=escalate_channel, text=reply, as_user=True)
    return
