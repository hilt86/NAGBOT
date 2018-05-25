import logging
from flask import json, jsonify, Response
import qanda
import json
import pprint
import os
from slackclient import SlackClient

# create logger
module_logger = logging.getLogger('nagbot.realert')

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
        self.logger.debug('Creating an instance of ReAlert')
        
    def receiveJSON(self, rxdataJSON):
        self.logger = logging.getLogger('nagbot.realert.ReAlert.receiveJSON')
        self.logger.debug('Receiving Data ...')        
        if rxdataJSON.headers['Content-Type'] == 'application/json':
            self.logger.debug('Receiving JSON Data ...')            
            jsonData = rxdataJSON.json
            # If json data is there pull it out.
            if jsonData["system"]["auth"]["ssh"]["ip"] and jsonData["system"]["auth"]["user"]:                
                self.logger.info(str("JSON Data - User {0} Detected on IP - {1}".format(jsonData["system"]["auth"]["user"].upper(), jsonData["system"]["auth"]["ssh"]["ip"])))                
                rtnData = jsonData["system"]["auth"]["ssh"]["ip"],jsonData["system"]["auth"]["user"],jsonData["system"]["auth"]["timestamp"]            
                return rtnData
            else:
                self.logger.info("JSON Data - Data No Detected")
                return None            
        else:
            self.logger.warning("Unsupported Media Type ;)")            
            return None
    
    # Write Data to File - For Auditing Purposes - If Required
    def writeJSONToFile(self, dataJSON):
        self.logger = logging.getLogger('nagbot.realert.ReAlert.writeJSONToFile')
        self.logger.info('Writing JSON Data to File ...')
        data = json.dumps(dataJSON)
        with open("nagbot.json","a") as f:
            f.write(data)
            f.write("\n")
        f.close()
