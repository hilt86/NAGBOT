def realert(alertJSON):
    """ function that receives the JSON response from flask and sends an 
        alert based on the end user's response to the question
    """
    """
    dustin receives json
    sorts through json to find user id
    
    uses qanda function to send message to user in id field
    waits for response
    sends another alert if no or timeout
    """