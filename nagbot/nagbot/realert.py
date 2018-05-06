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
        self.logger.info('Receiving JSON Data ...')
        if rxdataJSON.headers['Content-Type'] == 'application/json':
            #return "JSON Message: " + json.dumps(request.json)
            jsonData = rxdataJSON.json
            if jsonData['somefield'] == 'a':
                self.logger.info("JSON Data - Success")
                return "Success !!!"
            elif jsonData['somefield'] == 'b':
                self.logger.info("JSON Data - More Success")
                return "More Success !!!!"
            else:
                self.logger.info("JSON Data - Boo !!!")
                return "Boo !!!"
        else:
            self.logger.info("415 Unsupported Media Type ;)")
            return "415 Unsupported Media Type ;)"

def some_function():
    module_logger.info('received a call to "some_function"')