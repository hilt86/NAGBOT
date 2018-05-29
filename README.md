# CSC3600
## Semester 1 2018
This Repository is for a University of Southern Queensland (USQ) Undergraduate Subject - CSC3600

**Project Members** 

Hilton De Meillon

Dustin Lee

John Omer-Cooper

Bandr Talie O Alkhuzaie

## In this guide:
[**NAGBOT**](#nagbot)
- [Pre-requisites](#pre-requisites)
- [Installation](#installation)
 - [1. Deploy NagBot to a server or cloud service.](#1-deploy-nagbot-to-a-server-or-cloud-service)
 - [2. Setting up NagBot in Slack.](#2-setting-up-nagbot-in-slack)
  - [2.1 Create a NagBot Slack app.](#21-create-a-nagbot-slack-app-on-apislackcom)
  - [2.2 Tokens, Verification and Environmental variables.](#22-tokens-verification-and-environmental-variables)
  - [2.3 Create a channel to receive escalation events.](#23-create-a-channel-to-receive-escalation-events)
  - [2.4 Test it works.](#24-test-it-works)
 - [3. Good to go](#3-good-to-go)

# NAGBOT 

### Your security operations logs million of events, today we logged:

![39_millionevents](https://user-images.githubusercontent.com/37161577/40632771-e4adc3ca-632d-11e8-91c8-b2d7d481e9f5.png)

Events like this:

![kmitnick](https://user-images.githubusercontent.com/37161577/40632783-081a8b5e-632e-11e8-8514-697389810f38.png)


Is this something to be worried about, is this really kmitnick, why so many IP's, are they travelling, using a VPN, is your load balancer scaling to demand ... ?

How do you find this in a log with a million or more events ?

**NagBot can help.**

Project Nagbot is a Slack bot that hopes to solve the problem of sorting and detecting security events in large volumes of security data and make security alerting more manageable.

### Pre-requisites

1. Elasticsearch database 
2. Elastalert installation
3. Python runtime environment within which to run Nagbot
4. Slack

1. Elastalert uses or creates an elasticsearch index to store it's alert state. Occasionly this index will need to be deleted using elasticsearch management tools and the "elastalert-create-index" command line utility.

## Installation

## 1. Deploy NagBot to a server or cloud service.

#### More to come

## 2. Setting up NagBot in Slack.
### 2.1 Create a NagBot Slack app on [api.slack.com](https://api.slack.com/apps?utm_source=events&utm_campaign=build-bot-workshop&utm_medium=workshop)

To set up the NagBot app to work with Slack we need to create a Slack App for your workspace.
In your browser navigate to https://api.slack.com/apps . You will be presented with an option to create a new app.

![1_create_new_app](https://user-images.githubusercontent.com/37161577/40458776-3216e5ec-5f41-11e8-98b8-4b81be88d61f.png)

Select the friendly green button and create a new app.

Give the App a name "NagBot" and assign it to it's Workspace.

![2_app_name_workspace](https://user-images.githubusercontent.com/37161577/40458780-35bfd2c6-5f41-11e8-8685-6fb18bab1fc1.png)

To enable NagBot to interactively message the users of your workspace, Slack needs a *url* to send messages to and a *url* which define what actions to take. eg escalate an out of cardinality login.

Navigate to the Interactive Components in the left menu list.

![3_menu_list](https://user-images.githubusercontent.com/37161577/40458785-38d7920a-5f41-11e8-9150-d2fd3676b309.png)

Turn on interactivity, then fill in the **Request URL** and **Options Load URL** fields, with the URL home of your NagBot app followed by `/slack/message_options` in the request URL and `/slack/message_actions` in the Options Load URL field.

![4_turnon_interactivity](https://user-images.githubusercontent.com/37161577/40458788-3b6ce7ea-5f41-11e8-86f0-e2ce178506b9.png)

**Don’t forget to save changes.**

To make NagBot appear like a standard user in your workspace, set the **Bot User** details:

![5_botuser](https://user-images.githubusercontent.com/37161577/40458793-3eaf5730-5f41-11e8-83c5-61c3beed2c12.png)

**Don’t forget to save.**

##Event Escalation
Security personnel will receive messages in the escalation channel from the bot as you have named it here.

### 2.2 Tokens, Verification and Environmental variables.

So that Slack will accept message from your NagBot and can send messages back to Slack we need a:
**SLACK_BOT_TOKEN** called the Bot User OAuth Token.
**SLACK_VERIFICATION_TOKEN** conveniently enough call Verification Token.
It is important that these tokens remain secret, do not share them. 
To retrieve the **SLACK_BOT_TOKEN** 
Navigate to OAuth & Permissions in the left hand side menu:

![6_ oauth_token](https://user-images.githubusercontent.com/37161577/40458798-456db936-5f41-11e8-915c-48994c42efbf.png)

 Copy this to like named environmental variables on the server hosting your NagBot App.
 
eg. `$export SLACK_BOT_TOKEN=”xoxp-secret_token”`

To retrieve the **SLACK_VERIFICATION_TOKEN**

Navigate to Basic Information in the left hand side menu:

![7_verification_token](https://user-images.githubusercontent.com/37161577/40458803-4af1a96c-5f41-11e8-8bad-5502e7eb6a34.png)

 Copy this to like named environmental variables on the server hosting your NagBot App.
 
eg. `$export SLACK_VERIFICATION_TOKEN =”another secret token”`

### 2.3 Create a channel to receive escalation events.

Finally we need to create a Slack channel to which suspicious login events can be sent. Only administrative personnel and NagBot need access to this channel.
Create a channel, using either Slack app or the Slack Web site, in the workspace you wish NagBot to be active click the **+** next to Channels 

![8_addchannel](https://user-images.githubusercontent.com/37161577/40458806-4e29d1f4-5f41-11e8-8224-9bd04f23453a.png)

Fill in the displayed fields:
- change Public to Private if you want escalations to remain private.
- invite the users and NagBot.
- then Create Channel.

![9_escalatechannel](https://user-images.githubusercontent.com/37161577/40458808-50508572-5f41-11e8-9aac-407e65a4630b.png)

Additional users can always be added to the channel later.

NagBot needs to know where to send the escalation message this is identified by the channel id. 
The easiest way to find it is in the `url` field of your browser. Navigate to the slack channel and the channel id will appear after `/message/####`

eg. `https://yourserver.com/messages/ABCDEFGHI/`

Copy this to a NAGBOT_SLACK_CHANNEL environmental variable onto your server.

eg. `$export NAGBOT_SLACK_CHANNEL=”ABCDEFGHI”`

### 2.4 Test it works.

To test it generate an alert from Elastalert or use curl to send Nagbot a json test event.
For example:

#### test_event.json

`{
 "system": {
  "auth": {
   "hostname": "yourhost",
   "ssh": {
    "geoip": {
     "continent_name": "Oceania",
     "city_name": "Pakenham East",
     "country_iso_code": "AU",
     "region_name": "Victoria",
     "location": {
      "lon": 145.4741,
      "lat": -38.0702
     }
    },
    "method": "password",
    "port": "54084",
    "ip": "8.4.4.4",
    "event": "Accepted"
   },
   "pid": "8569",
   "user": "your user id",
   "timestamp": "May 18 02:34:24"
  }
 },
 "offset": 162887,
 "beat": {
  "hostname": "your elastic serach server",
  "name": " your elastic serach server ",
  "version": "6.2.3"
 },
 "prospector": {
  "type": "log"
 },
 "source": "/var/log/auth.log",
 "fileset": {
  "module": "system",
  "name": "auth"
 }
}`

From the command line use curl to send the json to NagBot

#### Curl command:

`curl -XPOST --header "Content-Type: application/json" 'https://yourserver.nagbotapp.com/api/json/nagbot/' -d @test_event.json`


### 3 Good to go.

That’s it NagBot should be ready to use.

NagBot will send messages directly to a user:

![10_nagbotmessage](https://user-images.githubusercontent.com/37161577/40458814-53a3ef7a-5f41-11e8-90a4-5f97ae3386bd.png)

Respond directly to the user if all is OK

Or 

Escalate the event to admin or security personnel via the designated escalation channel.

![11_securityalert](https://user-images.githubusercontent.com/37161577/40458815-5628e9f8-5f41-11e8-82b2-eae5cfbb9697.png)
