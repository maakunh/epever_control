#line_message.py
#line message ver 1.0 Update: 30/08/2021
#Author: Masafumi Hiura
#URL: https://github.com/maakunh/LINE_Messaging_API
#This code send LINE message. 
#LINE Messaging API is presented by LINE Corporation Japan.
#For detail, reffer to LINE Developers Docs
##https://developers.line.biz/en/docs/


import LINE_Messaging_API_setting
import datetime
import sys
import sqlite3

class line_message_db:
    def __init__(self):
        self.lvNormal = 0
        self.lvError = 1
        self.update_flg_linemsg_on = 2  #unsend
        self.update_flg_linemsg_off = 9 #sent
        self.update_flg_linemsg_ignore = 99 #ignore
    
    def read_line_message_maxnumber(self, dbPath):
        conn = sqlite3.connect(dbPath)
        cur = conn.cursor()

        try:
            cur.execute("SELECT MAX(number) FROM line_message")
            self.line_message_maxnumber = cur.fetchone()[0]
            ret = self.lvNormal
        except sqlite3.Error as e:
            print(e)
            ret = self.lvError
        conn.close()
        return ret

    def read_line_message_get_unsend_list(self, dbPath, update_flg):
        conn = sqlite3.connect(dbPath)
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM line_message WHERE update_flg = '" + str(update_flg) + "'")
            self.linemsg_send_list = cur.fetchall()
            ret = self.lvNormal
        except sqlite3.Error as e:
            print(e)
            ret = self.lvError
        conn.close()
        return ret

    def write_line_message_request(self, dbPath, update_flg, request_datetime, send_datetime, msg, number, application):
        conn = sqlite3.connect(dbPath)
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO line_message VALUES('" + str(update_flg) + "', '" + msg + "', '" + request_datetime + "', '" + send_datetime + "', " + str(number) + ", '" + application + "')")
            conn.commit()
            ret = self.lvNormal
        except sqlite3.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

    def update_line_message_flg(self, dbPath, update_flg, send_datetime, number):
        conn = sqlite3.connect(dbPath)
        cur = conn.cursor()
        try:
            cur.execute("UPDATE line_message SET update_flg = '" + str(update_flg) + "', send_datetime = '" + send_datetime + "' WHERE number = " + str(number))
            conn.commit()
            ret = self.lvNormal
        except sqlite3.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

class line_message_useAPI:
    def __init__(self):
        self.lvNormal = 0
        self.lvError = 1
        self.update_flg_linemsg_on = 2  #unsend
        self.update_flg_linemsg_off = 9 #sent
        self.update_flg_linemsg_ignore = 99 #ignore

    def post_message(self):
        #LINE Messaging API
        cls_Line_Messaging_API_setting = LINE_Messaging_API_setting.LINE_Messaging_API()

        #database
        cls_db = line_message_db()

        #Get unsend list
        ret = cls_db.read_line_message_get_unsend_list(cls_Line_Messaging_API_setting.line_message_db_path, cls_db.update_flg_linemsg_on)
        if ret == cls_db.lvNormal:
            ret = self.lvNormal
            unsend_list = cls_db.linemsg_send_list
            dt_now = datetime.datetime.now()
            for unsend in unsend_list:
                ret = cls_Line_Messaging_API_setting.post_messages(unsend[1]  + '\r\n' + " request date : " + unsend[2]+ '\r\n' + " application : " + unsend[5])
                if ret == cls_Line_Messaging_API_setting.lvNormal:
                    ret = cls_db.update_line_message_flg(cls_Line_Messaging_API_setting.line_message_db_path, self.update_flg_linemsg_off, dt_now.strftime('%Y/%m/%d %H:%M:%S'), unsend[4])
                    if ret == cls_db.lvError:
                        self.ret = self.lvError
        elif ret == cls_db.lvError:
            ret = self.lvError

        return ret

    def line_message_request(self, msg, application):
        #LINE Messaging API
        cls_Line_Messaging_API_setting = LINE_Messaging_API_setting.LINE_Messaging_API()

        #database
        cls_db = line_message_db()
        dt_now = datetime.datetime.now()
        ret = cls_db.read_line_message_maxnumber(cls_Line_Messaging_API_setting.line_message_db_path)
        if ret == cls_db.lvNormal:
            ret = cls_db.write_line_message_request(cls_Line_Messaging_API_setting.line_message_db_path, self.update_flg_linemsg_on, dt_now.strftime('%Y/%m/%d %H:%M:%S'), dt_now.strftime('%Y/%m/%d %H:%M:%S'), msg, cls_db.line_message_maxnumber + 1, application)
            if ret == cls_db.lvNormal:
                ret = self.lvNormal
            elif ret == cls_db.lvError:
                ret = self.lvError
        elif ret == cls_db.lvError:
            ret = self.lvError
        return ret


#this module test
#You can test LINE_Messaging_API_setting.py in command line console.
def Test():
    cls_LINE_Messaging_API = LINE_Messaging_API_setting.LINE_Messaging_API()
    print(cls_LINE_Messaging_API.CHANNEL_ACCESS_TOKEN)
    print(cls_LINE_Messaging_API.USER_ID)

    #send message request
    print("send message request")
    cls_useAPI = line_message_useAPI()
    cls_db = line_message_db()
    cls_db.read_line_message_maxnumber(cls_LINE_Messaging_API.line_message_db_path)
    print(cls_db.line_message_maxnumber)
    ret = cls_useAPI.line_message_request("test","TESTApp")
    print(ret)

    #post message
    print("post message for above request")
    cls_useAPI.post_message()


#Main
def Main():
    cls_useAPI = line_message_useAPI()
    #post message
    cls_useAPI.post_message()

if __name__ == '__main__':
    # Test()
    Main()