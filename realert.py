import logging
from flask import json, jsonify, Response
import qanda
import json
import pprint
import os
from slackclient import SlackClient

# create logger
module_logger = logging.getLogger('nagbot.realert')

# pp = pprint.PrettyPrinter(indent=4)

# Exception Class
class reAlertFailed(Exception):
    pass

# Main Class
class ReAlert:
    '''
    Responds to JSON Information sent from an Elastalert POST request.
    Init:
        :Args:
            Takes JSON Data from Elastalert and pulls out the IP and Username
            Then will utilise 'qanda' function to send Questions to userout of band in slack.
    '''
    def __init__(self):
        self.logger = logging.getLogger('nagbot.realert.ReAlert')
        self.logger.info('Creating an instance of ReAlert')

    def do_something(self):
        self.logger.info('ReAlert is doing something')
        a = 1 + 1
        self.logger.info('ReAlert has done something')
        
    def sendQanda(self, question):
        self.logger.info('Sending Data ...')
        # qanda(name, question, slack_client, slack_channel, nagbot_user_id, admin, resp_time):
        # qanda.qanda("<@U9JC2HE7R>", question, SlackClient(nagbotSlackBotToken), "CA69A9U8J", "UAMJZ591D", "<@U9JC2HE7R>", 60)
        
    def receiveJSON(self, rxdataJSON):
        self.logger.debug('Receiving Data ...')
        print('### Receiving Data ... ###')
        if rxdataJSON.headers['Content-Type'] == 'application/json':
            self.logger.debug('Receiving JSON Data ...')
            print('### Receiving JSON Data ... ###')
            jsonData = rxdataJSON.json
            if jsonData["system"]["auth"]["ssh"]["ip"] and jsonData["system"]["auth"]["user"]:
                elastalertData = str("JSON Data - User {0} Detected on IP - {1}".format(jsonData["system"]["auth"]["user"].upper(), jsonData["system"]["auth"]["ssh"]["ip"]))
                self.logger.info(elastalertData)
                print(elastalertData)
                # self.logger.info("JSON Data - User {0} Detected on IP - {1}".format(jsonData["system"]["auth"]["user"], jsonData["system"]["auth"]["ssh"]["ip"]))
                #self.sendQanda(str("Hello, " + jsonData["system"]["auth"]["user"].capitalize() + " did you login from " + jsonData["system"]["auth"]["ssh"]["ip"]))
                pass
            else:
                self.logger.info("JSON Data - Data No Detected")
                print('### JSON Data - Data No Detected ###')
                return None
            # rtnData = str(json.dumps([jsonData["system"]["auth"]["ssh"]["ip"],jsonData["system"]["auth"]["user"]]))
            # rtnData = (json.dumps([jsonData["system"]["auth"]["ssh"]["ip"],jsonData["system"]["auth"]["user"]]))
            rtnData = jsonData["system"]["auth"]["ssh"]["ip"],jsonData["system"]["auth"]["user"],jsonData["system"]["auth"]["timestamp"]
            # pp.pprint(rtnData)
            self.logger.info("Receiving JSON Data - {}".format(rtnData))
            return rtnData
        else:
            self.logger.warning("Unsupported Media Type ;)")
            print('### Unsupported Media Type ###')
            return None
    
    def writeJSONToFile(self, dataJSON):
        self.logger.info('Writing JSON Data to File ...')
        data = json.dumps(dataJSON)
        with open("nagbot.json","a") as f:
            f.write(data)
            f.write("\n")
        f.close()
