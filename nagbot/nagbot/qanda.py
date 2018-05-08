import logging
import json
from slackclient import SlackClient
import time
import pprint

pp = pprint.PrettyPrinter(indent=4)

# create logger
module_logger = logging.getLogger('nagbot.qanda')

# Exception Class
class qandaFailed(Exception):
    pass
class chatTimeOut(Exception):
    pass
class chatEscalate(Exception):
    pass

# Main Class
class QandA:
    '''
    QandA object that implements the Questioning and response questioning to the approrpriate User
    
    Init:
        :Args:
            name (str):
            question (str):
            slack_client (sc object):
            slack_channel (str):
            nagbot_user_id (str):
            admin (str):
    '''
    def __init__(self, name, question, slack_client, slack_channel, nagbot_user_id, admin, responseTimer):
        self.logger = logging.getLogger('nagbot.qanda.QandA')
        self.logger.debug('Creating an instance of QandA')
        # 
        self.name = name
        self.question = question
        self.sc = slack_client
        self.slack_channel = slack_channel
        self.nagbot_user_id = nagbot_user_id
        self.admin = admin
        self.responseTimer = responseTimer
        self.answer = ""
        print("Name is : {}".format(self.name))
        print("Question is : {}".format(self.question))
        print("Slack Client is : {}".format(self.sc))
        # pp.pprint(self.sc)
        print("Slack Channel is : {}".format(self.slack_channel))
        print("Nagbot User ID is : {}".format(self.nagbot_user_id))
        print("Admin is : {}".format(self.admin))
        print("Response Time is : {}".format(self.responseTimer))

    #def qanda(self, name, question, slack_client, slack_channel, nagbot_user_id, admin, responseTimer):
    def qanda(self):
        # This function sends and retrieves responses from Slack as nagbot to assigned users.
        # name - is the name of the target user.
        # question - the question requireing a yes or no answer.
        # slack_client - is the OAuth token reuired to communicate with Slack
        # slack_channel and nagbot_user - are the channel and bot user id's.
        # responseTimer - defines how long in sec a user has to respond befor admin is notified.
        
        # pp = pprint.PrettyPrinter(indent=4)
        
        # if self.sc.rtm_connect(with_team_state=False):
        if self.sc.rtm_connect():
            if self.sc.server.connected is True:
                self.logger.info("NagBot connected and running!")
            try:
                response = "Hi," + self.name + "\n"+ self.question
                # self.sc.api_call("chat.postMessage", channel=self.slack_channel, text=response, as_user=True)
                # pp.pprint(self.sc.api_call("api.test"))
                scResponse = self.sc.api_call("chat.postMessage", channel=self.slack_channel, text=response)
                # print("scResponse is :{}".format(type(scResponse)))
                # pp.pprint(scResponse)
                # Check to see if the message sent successfully.
                # If the message succeeded, `response["ok"]`` will be `True`
                if scResponse["ok"] == True:
                    print("Message posted successfully: " + scResponse["message"]["ts"])
                    # If the message failed, check for rate limit headers in the response
                while self.sc.server.connected is True:
                    if self.responseTimer <= 0:
                        raise chatTimeOut
                    # pp.pprint(self.sc.rtm_read())
                    newEvents = self.sc.rtm_read()
                    pp.pprint(newEvents), 
                    for event in newEvents:
                        pp.pprint(event), 
                        if "type" in event:
                            if event['type'] == "message" and event['channel'] == self.slack_channel:
                                if event['user'] != self.nagbot_user_id and "<@" + self.nagbot_user_id + ">" not in event['text']:
                                    user_info = self.sc.api_call("users.info", user=event['user'])
                                    #print(event['text'])
                                    self.logger.info(event['text'])
                                    answer = event['text']
                                    response = response_option(self.answer, self.name, self.sc, self.slack_channel, self.nagbot_user_id, self.admin, self.responseTimer)
                                    # slack_client.api_call("chat.postMessage", channel=event['channel'], text=response, as_user=True)
                                    slack_client.api_call("chat.postMessage", channel=event['channel'], text=response)
                                    return
                            if event['type'] == "hello":
                                print("GoodBye")
                    time.sleep(1)
                    self.responseTimer -=1
                    print(self.responseTimer),
            except chatTimeOut:
                reply = self.admin + " User " + self.name + " has not replied to login alert in acceptable timeframe"
                self.sc.api_call("chat.postMessage", channel=self.slack_channel, text=reply)
                self.logger.debug("Chat Response TimeOut")
            except chatEscalate:
                pass
                #  # This function defines what to do in the case of a negative response from a user. ie notify admin.
                # reply = self.admin + " This is a test, " + self.name + "s login could NOT be confirmed !"
                # self.sc.api_call("chat.postMessage", channel=self.slack_channel, text=reply, as_user=True)
                # reply=" "
                # return reply
            except:
                self.logger.info("Check QandA !")
        else:
            self.logger.error("Connection Failed ?")

    # def response_option(self, answer, name, slack_client, slack_channel, nagbot_user_id, admin, responseTimer):
    def response_option(self):
        # This function provides the actions based on user answers.
        if answer.lower() == "no":
            # escalate(self.admin, self.name, self.sc, self.slack_channel)
            escalate()
        elif answer.lower() == "yes":
            reply = "Great carry on !"
            return reply
        else:
            self.question = "Not sure what you mean. Please answer yes or no."
            # qanda(name, question, slack_client, slack_channel,nagbot_user_id, admin, responseTimer)
            # qanda()
            
    # Simple wrapper for sending a Slack message
    def send_slack_message(channel, message):
        return sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=message
        )
            
