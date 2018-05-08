import os
import time
from slackclient import SlackClient
import logging
import pprint

class chatTimeOut(Exception):
    pass

# slackToken = os.environ["NAGBOT_SLACK_BOT_TOKEN"]
slackToken = os.environ["CSC3600_TOKEN"]
print ("Slack Token is : {}".format(slackToken))

# Simple wrapper for sending a Slack message
def sendSlackMessage(sc, channel, message):
    return sc.api_call(
    "chat.postMessage",
    channel=channel,
    text=message,
    as_user='true:'
)

# def sendSlackMessage(sc, channel, message):
#     return sc.api_call(
#     "chat.postMessage",
#     channel=channel,
#     text=message
# )

class SlackComms:
    def __init__(self, slackToken):
        self.sc = SlackClient(slackToken)
        self.logger = logging.getLogger('test_slack.SlackComms')
        self.logger.info('Creating an instance of SlackComms')

    def sendMessage(self, channel, question, userId, responseTimer = 30):
        self.logger = logging.getLogger('test_slack.SlackComms.sendMessage')
        if self.sc.rtm_connect():
            self.logger.debug('Connecting ...')
            if self.sc.server.connected is True:
                self.logger.debug('Connected ...')
                self.logger.debug('Sending Message')
            response = sendSlackMessage(self.sc, channel, question)
            pp.pprint(response)
            # return
            try:
                while True:
                    if responseTimer <= 0:
                        raise chatTimeOut
                    # events = self.sc.rtm_read()
                    # pp.pprint(events)
                    # for event in events:
                    for event in self.sc.rtm_read():
                        if ('channel' in event and 'text' in event and event.get('type') == 'message'):
                            # if event['user'] != userId and "<@" + userId + ">" not in event['text']:
                            if event['user'] != userId:
                                    # self.logger.info('In the Loop !')
                                    userInfo = self.sc.api_call("users.info", user=event['user'])
                                    pp.pprint(userInfo)
                                    print("User Info is : {}".format(userInfo['id']))
                                    # self.logger.info("User Info is : {}".format(userInfo['id']))
                                    #print(event['text'])
                                    # self.logger.info(event['text'])
                                    # answer = event['text']
                                    # print(answer)
                                    # response = answerResponse(answer)
                                    # pp.pprint(response)
                                    # slack_client.api_call("chat.postMessage", channel=event['channel'], text=response, as_user=True)
                                    # self.sc.api_call("chat.postMessage", channel=event['channel'], text=response)
                                    self.logger.debug(event['text'])
                                    # pass
                        pp.pprint(event)
                    time.sleep(1)
                    responseTimer -=1
                    print(responseTimer),
                    # self.logger.info(responseTimer)
            except chatTimeOut:
                pass
            except:
                pass
        else:
            self.logger.info('Connection failed, invalid token?')

    def testMessage(self, channel, question, responseTimer = 30):
        if self.sc.rtm_connect():
            if self.sc.server.connected is True:
                self.logger.info('Creating an instance of SlackComms')
                # print("NagBot connected and running!")
            # Make the API call and save results to `response`
            # pp.pprint(sc.api_call("channels.list"))
            # response = sendSlackMessage("C9M9SN3DL", "Hello, from Python - Testing Slack Messaging!")
            # response = sendSlackMessage("C9M9SN3DL", self.question)
            response = sendSlackMessage(self.sc, channel, question)
            pp.pprint(response)
            try:
                while True:
                    if responseTimer <= 0:
                        raise chatTimeOut
                    events = self.sc.rtm_read()
                    pp.pprint(events)
                    for event in events:
                        if ('channel' in event and 'text' in event and event.get('type') == 'message'):
                            channel = event['channel']
                            print(channel), 
                            text = event['text']
                            print(text)
                            # if 'wassup' in text.lower() and link not in text:
                            if 'wassup' in text.lower():
                                sc.api_call(
                                    'chat.postMessage',
                                    channel=channel,
                                    text="You Know It !!!!",
                                    as_user='true:'
                                )
                    time.sleep(1)
                    responseTimer -=1
                    print(responseTimer),
            except chatTimeOut:
                pass
            except:
                pass
        else:
            self.logger.info('Connection failed, invalid token?')
            # print('Connection failed, invalid token?')
    
    def dumpChannelInfo(self):
        if self.sc.rtm_connect():
            if self.sc.server.connected is True:
                # print("SlackClient connected and running!")
                self.logger.info('SlackClient connected and running!')
                channelList = self.sc.api_call("channels.list")
                userList = self.sc.api_call("users.list")
                # pp.pprint(channelList)
                # pp.pprint([channel["id"] for channel in channelList["channels"]])
                # pp.pprint([channel["name"] for channel in channelList["channels"]])
                for channel in channelList["channels"]:
                    # print channel["id"],
                    # print channel["name"], 
                    print ("------------------------------------------------------------------------------")
                    print ("Channel : {0}\nID      : {1}\nPurpose : {2}\nTopic   : {3}\nMembers : {4}".format(channel["name"],channel["id"], channel["purpose"]["value"], channel["topic"]["value"], channel["num_members"]))
                    print ("Member  :"),
                    if not channel["members"]:
                        pass
                    else:
                        for member in channel["members"][:-1]:
                            print ("{0}".format(member)),
                        print ("{0}".format(channel["members"][-1]))
                print ("------------------------------------------------------------------------------")
                # pp.pprint(userList)
                for user in userList["members"]:
                    if not user["deleted"]:
                        print ("------------------------------------------------------------------------------")
                        # print ("Id           : {0}\nName         : {1}\nDisplay Name : {2}\nReal Name    : {3}\nDeleted      : {4}".format(user["id"], user["name"], user["profile"]["display_name"], user["profile"]["real_name"], user["deleted"]))
                        if not user["is_admin"]:
                            print ("Id           : {0}\nName         : {1}\nDisplay Name : {2}\nReal Name    : {3}".format(user["id"], user["name"], user["profile"]["display_name"], user["profile"]["real_name"]))
                        else:
                            print ("Id           : {0}\nName         : {1}\nDisplay Name : {2}\nReal Name    : {3}\nAdmin        : {4}".format(user["id"], user["name"], user["profile"]["display_name"], user["profile"]["real_name"], user["is_admin"]))
                    else:
                        pass
                print ("------------------------------------------------------------------------------")
        else:
            self.logger.info('Connection failed, invalid token?')
    
    def answerResponse(self, answer):
        # This function provides the actions based on user answers.
        if answer.lower() == "no":
            # escalate(self.admin, self.name, self.sc, self.slack_channel)
            # escalate()
            pass
        elif answer.lower() == "yes":
            reply = "Great carry on !"
            return reply
        else:
            pass


if __name__ == "__main__":
    # create logger
    logger = logging.getLogger('test_slack')
    logger.setLevel(logging.DEBUG)
    # Create Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # create console handler and set level to debug
    console = logging.StreamHandler()
    # This will take anything from DEBUG and Up
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(console)
    
    pp = pprint.PrettyPrinter(indent=4)

    question = "Hello there how are you ?"
    
    csc3600_playground = SlackComms(slackToken)
    csc3600_playground.sendMessage("C9M9SN3DL", question, 'UA2M06EH5', 60)