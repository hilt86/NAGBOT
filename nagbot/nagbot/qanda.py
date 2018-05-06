from slackclient import SlackClient
import time


def qanda(name, question, slack_client, slack_channel, nagbot_user_id, admin, resp_time):
     #This is the main question and answer function called from nagbot.py. It call slack_comm which calls other required funcitons.
    slack_comms(name, question, slack_client, slack_channel,nagbot_user_id,resp_time)
    
    
    
def slack_comms(name, question, slack_client, slack_channel,nagbot_user_id,resp_time):
    # This function sends and retrieves responses from Slack as nagbot to assigned users.
    # name is the name of the target user.
    # question the queestion requireing a yes or no answer.
    # slack_client is the OAuth token reuired to communicate with Slack
    # slack_channel and nagbot_user are the channel and bot user id's.
    # resp_time defines how long in sec a user has to respond befor admin is notified.
    if slack_client.rtm_connect():
        print("John Bot connected and running!")
        response = "Hi," + name + "\n"+ question
        slack_client.api_call("chat.postMessage", channel="CA69A9U8J", text=response, as_user=True)
        while True & resp_time >= 0:
            if resp_time == 0:
                time_out(admin, name)
            new_evts = slack_client.rtm_read()
            for evt in new_evts:
                if "type" in evt:
                    if evt['type']=="message" and evt['channel']=="CA69A9U8J":
                        if evt['user'] != "UA6DYQRFY" and "<@UA6DYQRFY>" not in evt['text']:
                            user_info=slack_client.api_call("users.info", user=evt['user'])
                            print(evt['text'])
                            answer=evt['text']
                            # response = response_option(answer)
                            response = response_option(answer, name, slack_client, slack_channel, "<@U9JC2HE7R>")
                            slack_client.api_call("chat.postMessage", channel=evt['channel'], text=response, as_user=True)
                            return
            time.sleep(1)
            resp_time -=1
    else:
        print "Connection Failed, invalid token?"

        
#def response_option(answer, name, admin, slack_client, slack_channel):
def response_option(answer, name, slack_client, slack_channel, admin):
    # This function provides the actions based on user answers.
    if answer.lower() == "no":
        escalate(admin, name, slack_client, slack_channel)
    elif answer.lower() == "yes":
        reply = "Great carry on !"
        return reply
    else:
        question = "Not sure what you mean. Please answer yes or no."
        slack_comms(name, question, slack_client, slack_channel,nagbot_user_id,resp_time)

def escalate(admin, name, slack_client, slack_channel):
    # This function defines what to do in the case of a negative response from a user. ie notify admin.
    reply = admin + " This is a test, " + name + "s login could be a sneaky little hobbitses !!!"
    slack_client.api_call("chat.postMessage", channel=slack_channel, text=reply, as_user=True)
    reply=" "
    return reply
    
def time_out(admin, name, slack_client, slack_channel):
    # This function defines what to do if the user does not respond iin the allocated time.
    reply = admin + " User " + name + " has not replied to login alert in acceptable timeframe"
    slack_client.api_call("chat.postMessage", channel=slack_channel, text=reply, as_user=True)
    reply=" "
    return reply
