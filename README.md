# DutchBot


## Setup
For this bot to work create 2 files in the root dir.

ApiKey.py
```Python
#!/usr/bin/env python3
API = '###APIKEYHERE###'
```
This is your Telegram Bot API key

BotDatabase
```
{ "Chats":[ { "id":"###CHATIDHERE###", "Keys":{ } }, { "id":"###CHATIDHERE###","Keys":{ } } ]}
```
This is the JsonDatabase the key/values are stored in.
For each Chat you wish this bot to work in you need to add a new Chat object:
```
{ "id":"###CHATIDHERE###", "Keys":{ } }
```
With ID beeing the Telegram Chat id
