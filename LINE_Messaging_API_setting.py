#LINE_Messaging_API_setting.py
#Author: Masafumi Hiura
#URL: https://github.com/maakunh/epever_control
#This code is imported by the code using LINE Messaging API
#LINE Messaging API is presented by LINE Corporation Japan.
#For detail, reffer to LINE Developers Docs
##https://developers.line.biz/en/docs/
#You write your environment parameters in this code.



import json
import urllib.request

class LINE_Messaging_API:
    def __init__(self):
        self.lvNormal = 0
        self.lvError = 1
        #these parameter is secret. DO NOT present to the public!!!
        self.CHANNEL_ACCESS_TOKEN = "Bearer {}"
        self.USER_ID = ""

        #LINE Messaging API urls
        ##Push Message(POST)
        self.LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push"

        ##Get Bot info(GET)
        self.LINE_BOT_INFO = "https://api.line.me/v2/bot/info"


    def post_messages(self, send_message):
        send_data = {"to": self.USER_ID, "messages": [{"type": "text", "text": send_message}]}
        jsonstr = json.dumps(send_data).encode()
        #post to LINE Messageing API
        headers = {'Content-Type':'application/json', 'Authorization':self.CHANNEL_ACCESS_TOKEN}
        req = urllib.request.Request(self.LINE_PUSH_URL, jsonstr, headers)

        #resoponse form Line Messaging API
        try:
            with urllib.request.urlopen(req) as res:
                self.body = res.read()
                ret = self.lvNormal
        except urllib.error.HTTPError as err:   #If error occured, set this parameter
            self.err_code = err.code
            ret = self.lvError

        return ret

    def get_bot_info(self):
        headers = {'Authorization':self.CHANNEL_ACCESS_TOKEN}
        req = urllib.request.Request('{}?{}'.format(self.LINE_BOT_INFO, urllib.parse.urlencode(headers)))   #Method: GET

        #resoponse form Line Messaging API
        try:
            with urllib.request.urlopen(req) as res:
                body = json.load(res)
                self.userId = body['userId']
                self.basicId = body['basicId']
                self.displayName = body['displayName']
                self.pictureUrl = body['pictureUrl']
                self.chatMode = body['chatMode']
                self.markAsReadMode = body['markAsReadMode']
                ret = self.lvNormal
        except urllib.error.HTTPError as err:   #If error occured, set this parameter
            self.err_code = err.code
            ret = self.lvError

        return ret
    
#this module test
#You can test LINE_Messaging_API_setting.py in command line console.
def Test():
    cls_LINE_Messaging_API = LINE_Messaging_API()
    print(cls_LINE_Messaging_API.CHANNEL_ACCESS_TOKEN)
    print(cls_LINE_Messaging_API.USER_ID)
    
    #Test push message
    ret = cls_LINE_Messaging_API.post_messages("Test!!!")
    if ret == cls_LINE_Messaging_API.lvNormal:
        print("push success!!!")
        print(ret)
    elif ret == cls_LINE_Messaging_API.lvError:
        print("HTTP Response error occured!!!")
        print(cls_LINE_Messaging_API.err_code)
    
    # #Test bot info
    # ret = cls_LINE_Messaging_API.get_bot_info()
    # if ret == cls_LINE_Messaging_API.lvNormal:
    #     print("userId = " + cls_LINE_Messaging_API.userId)
    #     print("basicId = " + cls_LINE_Messaging_API.basicId)
    #     print("displayName = " + cls_LINE_Messaging_API.displayName)
    #     print("pictureUrl = " + cls_LINE_Messaging_API.pictureUrl)
    #     print("chatMode = " + cls_LINE_Messaging_API.chatMode)
    #     print("markAsReadMode = " + cls_LINE_Messaging_API.markAsReadMode)
    # elif ret == cls_LINE_Messaging_API.lvError:
    #     print("HTTP Response error occured!!!")
    #     print(cls_LINE_Messaging_API.err_code)

if __name__ == '__main__':
    Test()