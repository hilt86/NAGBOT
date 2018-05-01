import os
import requests

from slackclient import SlackClient

SLACK_API_TOKEN = "xoxp-2319219074-324410592263-355519630176-aef7c53d42c8e8d2039c9bf04904ad69" # get one from https://api.slack.com/docs/oauth-test-tokens
CHANNEL_NAME = "nagbot_lives_here"
NAME = "Bandr"



    #This function finds the slack user id for a user subscribe to a designated channel
channel_list = requests.get('https://slack.com/api/channels.list?token=%s' % SLACK_API_TOKEN).json()['channels']
channel = filter(lambda c: c['name'] == CHANNEL_NAME, channel_list)[0]
channel_info = requests.get('https://slack.com/api/channels.info?token=%s&channel=%s' % (SLACK_API_TOKEN, channel['id'])).json()['channel']
members = channel_info['members']
users_list = requests.get('https://slack.com/api/users.list?token=%s' % SLACK_API_TOKEN).json()['members']
users = filter(lambda u: u['id'] in members, users_list)
    
for user in users:
    print(user['real_name'])
    print(user['id'])
    #first_name = user['real_name']
#if first_name == NAME:
    #print (first_name, user['id'])
#else:
 #   print ("Can't find them")
 
 

    