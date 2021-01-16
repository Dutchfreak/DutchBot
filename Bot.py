#!/usr/bin/env python3
import requests
import time
import re
import json
import ApiKey
LastUpdate = 0

APIAdd = f"https://api.telegram.org/bot{ApiKey.API}/"
def AddAction(message):
    Database = open("./BotDatabase","r")
    DBjson = json.loads(Database.read())
    Database.close()
    for Chat in DBjson["Chats"]:
        if  int(Chat["id"]) == int(message["chat"]["id"]):
            Text = message["text"]
            Splits = re.split("\s",Text)
            if len(Splits) < 4:
                return
            Value = ""
            for i in range(3,len(Splits)):
                Value = f'{Value} {Splits[i]}'

            Chat["Keys"][Splits[2].lower()] =Value
            Database = open("BotDatabase","w")
            Database.write(json.dumps(DBjson))
            Database.close()
            PostResponse(Chat["id"],f'Added key word:{Splits[2].lower()} with Value:{Value}')


def RemoveAction(message):
    Database = open("./BotDatabase","r")
    DBjson = json.loads(Database.read())
    Database.close()
    for Chat in DBjson["Chats"]:
        if  int(Chat["id"]) == int(message["chat"]["id"]):
            Text = message["text"]
            Splits = re.split("\s",Text)
            Chat["Keys"].pop(Splits[2], None)
            Database = open("BotDatabase","w")
            Database.write(json.dumps(DBjson))
            Database.close()
            PostResponse(Chat["id"],f'Removed key word:{Splits[2].lower()}')

def ListKeys(message):
    Database = open("./BotDatabase","r")
    DBjson = json.loads(Database.read())
    Database.close()
    for Chat in DBjson["Chats"]:
        if  int(Chat["id"]) == int(message["chat"]["id"]):
            List = "All Keys for this chat:\n*Key*%3A Value\n"
            for key,value in Chat["Keys"].items():
                List = f'{List}\n*{key}*%3A {EscapeText(value)}'
            PostResponse(Chat["id"],List,True)

def ParseMessage(message):
    Text = message["text"]
    Splits = re.split("\s",Text)
    if(Splits[1].lower() == "add"):
        AddAction(message)
    if(Splits[1].lower() == "remove"):
        RemoveAction(message)
    if(Splits[1].lower() == "list"):
        ListKeys(message)


def IsinChat(message):
    Database = open("./BotDatabase","r")
    DBjson = json.loads(Database.read())
    Database.close()
    for Chat in DBjson["Chats"]:
        if  int(Chat["id"]) == int(message["chat"]["id"]):
            return True
    return False

def EscapeText(text):
    ret= re.sub(r'([_*[\]()~`><#+\-=|{}.!])',r'\\\1',text)
    print (ret)
    return ret

def PostResponse(Chatid,Text,Markdown =False,Sender =""):
    if Markdown:
        Result = requests.get(f'{APIAdd}sendmessage?chat_id={Chatid}&parse_mode=MarkdownV2&text={Text}')
    else:
        if bool(re.search("{op}",Text)):
            print(Text.replace("{op}",Sender))
            Result = requests.get(f'{APIAdd}sendmessage?chat_id={Chatid}&text={Text.replace("{op}",Sender)}')
        else:
            print(Text)
            Result = requests.get(f'{APIAdd}sendmessage?chat_id={Chatid}&text={Text}')

def MatchMessage(message):
    Database = open("./BotDatabase","r")
    DBjson = json.loads(Database.read())
    Database.close()
    for Chat in DBjson["Chats"]:
        if  int(Chat["id"]) == int(message["chat"]["id"]):
            for key,value in Chat["Keys"].items():
                if bool(re.search(key.lower(),message["text"].lower())):
                    print(message["text"].lower())
                    PostResponse(message["chat"]["id"],value,False,message["from"]["username"])

while True:

    Result = requests.get(f'{APIAdd}getUpdates?offset={LastUpdate}')
    Updates = Result.json()
    #print (f'{APIAdd}getUpdates?offset={LastUpdate}')
    for Update in Updates["result"]:
        LastUpdate = Update["update_id"]+1
        if "text" in Update["message"]:
            Text = Update["message"]["text"]
            if bool(re.search("^/dutchbot ",Text.lower())):
                #print(f'Chat:{Update["message"]["chat"]["title"]} Id:{Update["message"]["chat"]["id"]} Message:{Update["message"]["text"]}')
                ParseMessage(Update["message"])
            else:
                if IsinChat(Update["message"]):
                    MatchMessage(Update["message"])

    time.sleep(.1000)
