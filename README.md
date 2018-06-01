
## In this guide:
[**NAGBOT**](#nagbot)
- [Pre-requisites](#pre-requisites)
- [Installation](#installation)
 - [1. Deploy NagBot to a server or cloud service.](#1-deploy-nagbot-to-a-server-or-cloud-service)
 - [2. Setting up NagBot in Slack.](#2-setting-up-nagbot-in-slack)
  - [2.1 Create a NagBot Slack app.](#21-create-a-nagbot-slack-app-on-apislackcom)
  - [2.2 Tokens, Verification and Environmental variables.](#22-tokens-verification-and-environmental-variables)
  - [2.3 Create a channel to receive escalation events.](#23-create-a-channel-to-receive-escalation-events)
  - [2.4 Manual test](#24-manual-test)
 - [3. Integration test](#3-integration-test)
 - [4. Credits](#4-credits)


### Is your security operations team faced with finding a needle within a haystack? 

In dynamic, multi-cloud deployments developers and security operations are faced with millions of security events every day. It is not uncommon for a log aggregation or SIEM system to have billions or even trillions of events which very quickly becomes unmanageable, for example :

```
May 28 11:18:19 elastic01 sshd[27085]: Failed password for jamesm from 74.45.57.208 port 61506 ssh2
May 28 23:37:23 elastic01 sshd[28450]: Accepted publickey for kevinm from 45.83.25.161 port 36578 ssh2: RSA SHA256:38jf892f9h2398fp982hf398h23f9
May 28 23:37:25 elastic01 sshd[28568]: Accepted publickey for kevinm from 50.18.27.141 port 27347 ssh2: RSA SHA256:38jf892f9h2398fp982hf398h23f9
May 28 23:37:34 elastic01 sshd[28634]: Accepted publickey for kevinm from 41.77.79.74 port 36000 ssh2: RSA SHA256:38jf892f9h2398fp982hf398h23f9
May 28 23:37:43 elastic01 sshd[28699]: Accepted publickey for kevinm from 104.163.162.211 port 39204 ssh2: RSA SHA256:38jf892f9h2398fp982hf398h23f9
May 28 23:37:52 elastic01 sshd[28764]: Accepted publickey for kevinm from 45.32.7.130 port 31533 ssh2: RSA SHA256:38jf892f9h2398fp982hf398h23f9
May 28 23:40:23 elastic01 sshd[28831]: Failed publickey for kevinm from 140.18.227.141 port 59899 ssh2: RSA SHA256:89asdlajksdas71ufhiol3fhsidfh
May 29 01:39:28 elastic01 sshd[26894]: Accepted password for jamesm from 8.45.7.8 port 49902 ssh2
```


Often the first thing security teams do is install a centralized logging system - which is a good step - but it quickly leads to log fatigue, where security analysts are overwhelmed by the amount of information they need to analyze. 

As the security program for an organization grows teams eventually put in place measures to reduce or filter failed logins using a VPN which means that there are less failed authorization attempts to sort through, but is this the best we can do?


# Introducing Nagbot

Our project, dubbed Nagbot takes this a step further and extends what is quickly becoming the industry standard logging and alerting (Elasticsearch + Elastalert) to further scrutinize successful logins. 

On successful SSHD login NagBot will send messages directly to the authenticated user using Slack :

![10_nagbotmessage](https://user-images.githubusercontent.com/37161577/40458814-53a3ef7a-5f41-11e8-90a4-5f97ae3386bd.png)


The user then selects a response from the dropdown "That was me" or "Wasn't me!" and Nagbot takes appropriate action. If the user responds "Wasn't me" Nagbot escalates the event to a separate Slack channel dedicated to security incidents:


![11_securityalert](https://user-images.githubusercontent.com/37161577/40458815-5628e9f8-5f41-11e8-82b2-eae5cfbb9697.png)

The best bit about Nagbot is it is licensed under an open source license so it can be easily deployed without any software licensing. 

### Pre-requisites

1. Elasticsearch database 
2. Elastalert installation
3. Python runtime environment within which to run Nagbot
4. Slack

1. Elastalert uses or creates an elasticsearch index to store it's alert state. Occasionly this index will need to be deleted using elasticsearch management tools and the "elastalert-create-index" command line utility.

## Installation

## 1. Deploy NagBot to a server or cloud service.

### 1.1 HEROKU Web Service

#### Clone NAGBOT Repository
```shell
git clone https://github.com/hilt86/NAGBOT.git
cd NAGBOT
```

#### Install App to Heroku
```shell
heroku create
```

#### Add the following settings to the Heroku Dashboard for your App

Settings --> Config Vars

| Config Var                        | Value                                     |
| -------------                     | -------------                             |
| DEBUG                             | \< True \| False \>                       |
| NAGBOT_SLACK_BOT_TOKEN            | \< Bot Token From Slack \>                |
| NAGBOT_SLACK_CHANNEL              | \< Slack Channel ID \>                    |
| NAGBOT_SLACK_ESCALATE_CHANNEL     | \< Slack Security/Escalation Channel ID \>|
| NAGBOT_SLACK_VERIFICATION_TOKEN   | \< Slack Verification Token \>            |
| NAGBOT_USER_ID                    | \< Slack Nagbot User ID \>                |


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

### 2.4 Manual test

To test slackbot manually generate an alert from Elastalert or use curl to send Nagbot a json test event.

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
      "lon": 141.4741,
      "lat": -34.0702
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
  "hostname": "your.elastic.search.server",
  "name": " your.elastic.search.server ",
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


### 3 Integration test

Now that you have tested the components you should be able to login to one of your systems monitored by Logstash / Elasticsearch from a few different IP addresses and you should get a challenge by Nagbot :


![10_nagbotmessage](https://user-images.githubusercontent.com/37161577/40458814-53a3ef7a-5f41-11e8-90a4-5f97ae3386bd.png)


The user then selects a response from the dropdown "That was me" or "Wasn't me!" and Nagbot takes appropriate action. If the user responds "Wasn't me" Nagbot escalates the event to a separate Slack channel dedicated to security incidents:


![11_securityalert](https://user-images.githubusercontent.com/37161577/40458815-5628e9f8-5f41-11e8-82b2-eae5cfbb9697.png)

### 4 Credits

Original concept from [Ryan Huber](https://slack.engineering/distributed-security-alerting-c89414c992d6) but he took too long to open source his version so we decided to make our own!

This project is a student project for a [University of Southern Queensland](https//www.usq.edu.au) Undergraduate Subject  CSC3600. Any opinions expressed are our own and do not necessarily represent policy of USQ.

**Project Members** 

[Hilton De Meillon](https://github.com/hilt86)

[Dustin Lee](https://github.com/Dustin-USQ)

[John Omer-Cooper](https://github.com/johno-c)

[Bandr Talie O Alkhuzaie](https://github.com/bandru1078238)
