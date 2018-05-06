import logging
import json
import pprint

# create logger
module_logger = logging.getLogger('nagbot.realert')
# Test Datastore
testJSONDatastore = {
                        "firstName": "Jane",
                        "lastName": "Doe",
                        "hobbies": ["running", "sky diving", "singing"],
                        "age": 35,
                        "children": [
                            {
                                "firstName": "Alice",
                                "age": 6
                            },
                            {
                                "firstName": "Bob",
                                "age": 8
                            }
                        ]
                    }

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

def some_function():
    module_logger.info('received a call to "some_function"')