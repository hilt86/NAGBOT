import logging
from flask import json, jsonify
import qanda
import json
import pprint

# create logger
module_logger = logging.getLogger('nagbot.realert')

# Exception Class
class reAlertFailed(Exception):
    pass

# Main Class
class ReAlert:
    '''
    The SlackClient makes API Calls to the `Slack Web API <https://api.slack.com/web>`_ as well as
    managing connections to the `Real-time Messaging API via websocket <https://api.slack.com/rtm>`_
    It also manages some of the Client state for Channels that the associated token (User or Bot)
    is associated with.
    For more information, check out the `Slack API Docs <https://api.slack.com/>`_
    Init:
        :Args:
            token (str): Your Slack Authentication token. You can find or generate a test token
            `here <https://api.slack.com/docs/oauth-test-tokens>`_
            Note: Be `careful with your token <https://api.slack.com/docs/oauth-safety>`_
            proxies (dict): Proxies to use when create websocket or api calls,
            declare http and websocket proxies using {'http': 'http://127.0.0.1'},
            and https proxy using {'https': 'https://127.0.0.1:443'}
    '''
    def __init__(self):
        self.logger = logging.getLogger('nagbot.realert.ReAlert')
        self.logger.info('creating an instance of ReAlert')

    def do_something(self):
        self.logger.info('ReAlert is doing something')
        a = 1 + 1
        self.logger.info('ReAlert has done something')
        
    def sendQanda(self):
        self.logger.info('Sending Data ...')
        # qanda(name, question, slack_client, slack_channel, nagbot_user_id, admin, resp_time):
        
    def receiveJSON(self, rxdataJSON):
        #self.logger.info('Receiving JSON Data ...')
        if rxdataJSON.headers['Content-Type'] == 'application/json':
            jsonData = rxdataJSON.json
            if jsonData["system"]["auth"]["ssh"]["ip"]:
                self.logger.info("JSON Data - IP Detected - {}".format(jsonData["system"]["auth"]["ssh"]["ip"]))
                pass
            elif jsonData["system"]["auth"]["user"]:
                self.logger.info("JSON Data - Username Detected - {}".format(jsonData["system"]["auth"]["user"]))
                pass
            else:
                self.logger.info("JSON Data - Data No Detected")
                return None
            rtnData = str(json.dumps([jsonData["system"]["auth"]["ssh"]["ip"],jsonData["system"]["auth"]["user"]]))
            self.logger.info("Receiving JSON Data - {}".format(rtnData))
            return rtnData
        else:
            self.logger.info("Unsupported Media Type ;)")
            # return "415 Unsupported Media Type ;)"
            # return str(json.dumps(jsonData))
            # rtnData = str(json.dumps([jsonData["system"]["auth"]["ssh"]["ip"],jsonData["system"]["auth"]["user"]]))
            # self.logger.info("Receiving JSON Data - {}".format(rtnData))
            return None
    
    def writeJSONToFile(self, dataJSON):
        self.logger.info('Writing JSON Data to File ...')
        data = json.dumps(dataJSON)
        with open("nagbot.json","a") as f:
            f.write(data)
            f.write("\n")
        f.close()

def some_function():
    module_logger.info('received a call to "some_function"')