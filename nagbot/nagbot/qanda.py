from slackclient import SlackClient



    
def qanda(name, question, slack_client):
    # This function takes two arguments a name and a question. It interacts with the user on a terminal command line.
    # It addresses the user by name and asks the passed question. It returns the answer which is printed to the terminal.  
    if slack_client.rtm_connect():
        print("John Bot connected and running!")
        response = "Hi," + name + "\n"+ question
        slack_client.api_call("chat.postMessage", channel="CA69A9U8J", text=response, as_user=True)
        while True:
            new_evts = slack_client.rtm_read()
            for evt in new_evts:
                if "type" in evt:
                    if evt['type']=="message" and evt['channel']=="CA69A9U8J":
                        if evt['user'] != "UA6DYQRFY" and "<@UA6DYQRFY>" not in evt['text']:
                            user_info=slack_client.api_call("users.info", user=evt['user'])
                            print(evt['text'])
                            answer=evt['text']
                            response = response_option(answer)
                            slack_client.api_call("chat.postMessage", channel=evt['channel'], text=response, as_user=True)
    else:
        print "Connection Failed, invalid token?"
        
def response_option(answer):
    if answer.lower() == "no":
        escalate(admin, name)

    else:
        reply = "Great carry on !"
    return reply

def escalate(admin, name):
    reply = " This is a test, Houston we have a problem with" + name + " login thanks John"
    qanda(admin, reply)