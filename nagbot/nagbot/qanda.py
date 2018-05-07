import logging
import json
from slackclient import SlackClient
import time

# create logger
module_logger = logging.getLogger('nagbot.qanda')

# Exception Class
class qanadaFailed(Exception):
    pass

# Main Class
class QandA:
    def __init__(self, name, question, slack_client, slack_channel, nagbot_user_id, admin, resp_time):
        self.logger = logging.getLogger('nagbot.qanda.QandA')
        self.logger.debug('Creating an instance of QandA')
        
        self.name = name
        self.question = question
        self.slack_client = slack_client
        self.slack_channel = slack_channel
        self.nagbot_user_id = nagbot_user_id
        self.admin = admin
        self.resp_time = resp_time
        self.answer = ""
    

    #def qanda(self, name, question, slack_client, slack_channel, nagbot_user_id, admin, resp_time):
    def qanda(self):
        # This function sends and retrieves responses from Slack as nagbot to assigned users.
        # name - is the name of the target user.
        # question - the question requireing a yes or no answer.
        # slack_client - is the OAuth token reuired to communicate with Slack
        # slack_channel and nagbot_user - are the channel and bot user id's.
        # resp_time - defines how long in sec a user has to respond befor admin is notified.
        if self.slack_client.rtm_connect():
            self.logger.info("NagBot connected and running!")
            response = "Hi," + self.name + "\n"+ self.question
            slack_client.api_call("chat.postMessage", channel=self.slack_channel, text=response, as_user=True)
            while True & self.resp_time >= 0:
                if self.resp_time == 0:
                    time_out(self.admin, self.name, self.slack_client, self.slack_channel)
                new_evts = slack_client.rtm_read()
                for evt in new_evts:
                    if "type" in evt:
                        if evt['type']=="message" and evt['channel'] == self.slack_channel:
                            if evt['user'] != self.nagbot_user_id and "<@" + self.nagbot_user_id + ">" not in evt['text']:
                                user_info=slack_client.api_call("users.info", user=evt['user'])
                                #print(evt['text'])
                                self.logger.info(evt['text'])
                                answer=evt['text']
                                response = response_option(answer, name, slack_client, slack_channel, nagbot_user_id, admin, resp_time)
                                slack_client.api_call("chat.postMessage", channel=evt['channel'], text=response, as_user=True)
                                return
                time.sleep(1)
                self.resp_time -=1
        else:
            #print "Connection Failed, invalid token?"
            self.logger.error("Connection Failed, invalid token?")


    # def response_option(self, answer, name, slack_client, slack_channel, nagbot_user_id, admin, resp_time):
    def response_option(self):
        # This function provides the actions based on user answers.
        if answer.lower() == "no":
            # escalate(self.admin, self.name, self.slack_client, self.slack_channel)
            escalate()
        elif answer.lower() == "yes":
            reply = "Great carry on !"
            return reply
        else:
            self.question = "Not sure what you mean. Please answer yes or no."
            # qanda(name, question, slack_client, slack_channel,nagbot_user_id, admin, resp_time)

    # def escalate(self, admin, name, slack_client, slack_channel):
    def escalate(self):
        # This function defines what to do in the case of a negative response from a user. ie notify admin.
        reply = self.admin + " This is a test, " + self.name + "s login could NOT be confirmed !"
        self.slack_client.api_call("chat.postMessage", channel=self.slack_channel, text=reply, as_user=True)
        reply=" "
        return reply
        
    # def time_out(self, admin, name, slack_client, slack_channel):
    def time_out(self):
        # This function defines what to do if the user does not respond in the allocated time.
        reply = self.admin + " User " + self.name + " has not replied to login alert in acceptable timeframe"
        self.slack_client.api_call("chat.postMessage", channel=self.slack_channel, text=reply, as_user=True)
        reply=" "
        return reply
