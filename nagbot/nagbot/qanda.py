import time
import logging


# create logger
# module_logger = logging.getLogger('nagbot.realert.qanda')

logger = logging.getLogger('nagbot.realert.qanda')
logger.info('QANDA')


def qanda(user_id, ip_add, slack_client, slack_channel, nagbot_user_id, admin, resp_time):
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
    question="Have you just logged in from "+ip_add+" ? yes or no "
    if slack_client.rtm_connect():
        logger.debug('qanda')
        print("NagBot connected and running!")
        response = "Hi," + name + "\n"+ question
        slack_client.api_call("chat.postMessage", channel=slack_channel, text=response, as_user=True)
        while True & resp_time >= 0:
            if resp_time == 0:
                time_out(admin_user, name, slack_client, slack_channel)
                return
            new_evts = slack_client.rtm_read()
            for evt in new_evts:
                if "type" in evt:
                    if evt['type']=="message" and evt['channel']==slack_channel:
                        if evt['user'] == user_id and evt['user'] != admin and "<@" + nagbot_user_id + ">" not in evt['text']:
                            user_info=slack_client.api_call("users.info", user=evt['user'])
                            answer=evt['text']
                            response = response_option(answer, name, admin_user, slack_client, slack_channel, nagbot_user_id,resp_time)
                            slack_client.api_call("chat.postMessage", channel=evt['channel'], text=response, as_user=True)
                            return
            time.sleep(1)
            resp_time -=1
    else:
        print "Connection Failed, invalid token?"
        logger.warning("Connection Failed, invalid token?")
        
def askQuestion(name, question, slack_client, slack_channel, nagbot_user_id, admin, resp_time):
    if slack_client.rtm_connect():
        response = name + question
        slack_client.api_call("chat.postMessage", channel=slack_channel, text=response, as_user=True)
    else:
        print "Connection Failed, invalid token?"
        logger.warning("Connection Failed, invalid token?")
    return

def grabResponses(name, slack_client, slack_channel, nagbot_user_id ):
    if slack_client.rtm_connect():
        slack_client.api_call("chat.postMessage", channel=slack_channel, text="Hello from Python! :tada:",
        user=name)
        print "got here"
        logger.debug("got here")
    else:
        logger.warning("Connection Failed, invalid token?")
        print "Connection Failed, invalid token?"
"""
 ? don't need this unless we want to dynamically retrieve user names from Slack.
 
def listUsers(name, question, slack_client, slack_channel, nagbot_user_id, admin, resp_time):
    if slack_client.rtm_connect():
        channel_list = requests.get('https://slack.com/api/channels.list?token=%s' % SLACK_API_TOKEN).json()['channels']
        channel = filter(lambda c: c['name'] == CHANNEL_NAME, channel_list)[0]
        channel_info = requests.get('https://slack.com/api/channels.info?token=%s&channel=%s' % (SLACK_API_TOKEN, channel['id'])).json()['channel']
        members = channel_info['members']
        users_list = requests.get('https://slack.com/api/users.list?token=%s' % SLACK_API_TOKEN).json()['members']
        users = filter(lambda u: u['id'] in members, users_list)
    
    for user in users:
        print(user['real_name'])
        print(user['id'])
    else:
        print "Connection Failed, invalid token?"
    return
"""

def response_option(answer, name, admin_user, slack_client, slack_channel, nagbot_user_id,resp_time):
    # This function provides the actions based on user answers.
    if answer.lower() == "no":
        escalate(name, slack_client, slack_channel)
    elif answer.lower() == "yes":
        reply = "Great carry on !"
        return reply
    else:
        question = "Not sure what you mean. Please answer yes or no."
        qanda(name, question, slack_client, slack_channel, nagbot_user_id, admin, resp_time)

def escalate(name, slack_client, slack_channel):
    logger.warning("Escalation Detected !")
    # This function defines what to do in the case of a negative response from a user. ie notify admin.
    reply =  " This is a test, " + name + "s login requires attention !!!"
    slack_client.api_call("chat.postMessage", channel=slack_channel, text=reply, as_user=True)
    reply=" "
    return reply
    
def time_out(admin_user, name, slack_client, slack_channel):
    # This function defines what to do if the user does not respond iin the allocated time.
    reply = admin_user + " User " + name + " has not replied to login alert in acceptable timeframe"
    slack_client.api_call("chat.postMessage", channel=slack_channel, text=reply, as_user=True)
    return