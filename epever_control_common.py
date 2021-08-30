#epever_control_common.py
#epever control ver 2.0 Update: 27/08/2021
## Modified: 28/08/2021
#Author: Masafumi Hiura
#URL: https://github.com/maakunh/epever_control
#This code is the common parameter/function of epever_control 

import time
import datetime
import time
import sqlite3
import re

import epever_control_setting

# import EPsolarTracerClient
from pyepsolartracer.client import EPsolarTracerClient
from pyepsolartracer.registers import registers,coils
# import the server implementation
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.mei_message import *
from pyepsolartracer.registers import registers,coils
import serial.rs485

class epever_control_commonvalue:
     def __init__(self):
        self.lvNormal = 0
        self.lvError = 1
        # self.update_flg_linemsg_on = 2
        # self.update_flg_linemsg_off = 9
        # self.update_flg_linemsg_ignore = 99
         
class epever_control_db:
    def __init__(self):
        cls_epever_control_common = epever_control_commonvalue()
        self.lvNormal = cls_epever_control_common.lvNormal
        self.lvError = cls_epever_control_common.lvError
        self.dbPath = epever_control_setting.epever_control_dbpath()
        self.dt_now = datetime.datetime.now()
        # self.line_message_enable = epever_control_setting.line_message_enable()
        # self.line_message_dbPath = epever_control_setting.line_message_dbpath()

    def read_control_nums(self, dbPath):
        conn = sqlite3.connect(dbPath)
        cur = conn.cursor()
        try:
            cur.execute("SELECT num FROM control")
            self.numlist = cur.fetchall()
            ret = self.lvNormal
        except sqlite3.Error as e:
            print(e)
            ret = self.lvError
        conn.close()
        return ret

    def read_control(self, dbPath, ctrlNum):
        conn = sqlite3.connect(dbPath)
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM control WHERE num =" + str(ctrlNum))
            self.lstCtrl = cur.fetchone()
            ret = self.lvNormal
        except sqlite3.Error as e:
            print(e)
            ret = self.lvError
    
        conn.close()

        #set result values
        self.Vmax = float(self.lstCtrl[1])
        self.Vmin = float(self.lstCtrl[2])
        self.Startime = datetime.datetime(year=int(self.dt_now.strftime('%Y')), month=int(self.dt_now.strftime('%m')), day=int(self.dt_now.strftime('%d')), hour=int(self.lstCtrl[3].strip()[:2]),  minute=int(self.lstCtrl[3].strip()[2:]))
        self.Endtime = self.Startime + datetime.timedelta(hours=int(self.lstCtrl[4][:2]),  minutes=int(self.lstCtrl[4][2:]))
        self.Relay1 = self.lstCtrl[5]
        self.Relay2 = self.lstCtrl[6]
        self.Relay3 = self.lstCtrl[7]
    
        return ret
    
    def write_control_history(self, dbPath, lvalue):
        conn = sqlite3.connect(dbPath)
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO control_history VALUES(?, ?, ?, ?, ?)", lvalue)
            conn.commit()
            ret = self.lvNormal
        except sqlite3.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret
    
    def read_colname(self, dbPath):
        conn = sqlite3.connect(dbPath)
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM colname")
            self.lstColname = cur.fetchone()
            ret = self.lvNormal
        except sqlite3.Error as e:
            print(e)
            ret = self.lvError
    
        conn.close()
        return ret

    def write_recordall(self, dbPath, lvalue):
        conn = sqlite3.connect(dbPath)
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO recordall VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", lvalue)
            conn.commit()
            ret = self.lvNormal
        except sqlite3.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret
    
    # def read_line_message_maxnumber(self, dbPath):
    #     conn = sqlite3.connect(dbPath)
    #     cur = conn.cursor()

    #     try:
    #         cur.execute("SELECT MAX(number) FROM line_message")
    #         self.line_message_maxnumber = cur.fetchone()[0]
    #         ret = self.lvNormal
    #     except sqlite3.Error as e:
    #         print(e)
    #         ret = self.lvError
    #     conn.close()
    #     return ret

    # def read_line_message_unsend_to_on(self, dbPath, update_flg):
    #     conn = sqlite3.connect(dbPath)
    #     cur = conn.cursor()

    #     try:
    #         cur.execute("SELECT * FROM line_message WHERE update_flg = '" + str(update_flg) + "'")
    #         self.linemsg_send_list = cur.fetchall()
    #         ret = self.lvNormal
    #     except sqlite3.Error as e:
    #         print(e)
    #         ret = self.lvError
    #     conn.close()
    #     return ret

    # def write_line_message(self, dbPath, update_flg, request_datetime, send_datetime, msg, number):
    #     conn = sqlite3.connect(dbPath)
    #     cur = conn.cursor()
    #     strList = list()
    #     # strList = strList.append(update_flg)
    #     # strList = strList.append(msg)
    #     # strList = strList.append(request_datetime)
    #     # strList = strList.appned(send_datetime)
    #     # strList = strList.append(number)
    #     print(update_flg)
    #     print(request_datetime)
    #     print(send_datetime)
    #     print(msg)
    #     print(number)
    #     try:
    #         cur.execute("INSERT INTO line_message VALUES('" + str(update_flg) + "', '" + msg + "', '" + request_datetime + "', '" + send_datetime + "', " + str(number) + ")")
    #         conn.commit()
    #         ret = self.lvNormal
    #     except sqlite3.Error as e:
    #         print(e)
    #         ret = self.lvError

    #     conn.close()
    #     return ret

    # def update_line_message_unsent_to_sent(self, dbPath, send_datetime, number):
    #     cls_epever_control_common = epever_control_commonvalue()
        
    #     conn = sqlite3.connect(dbPath)
    #     cur = conn.cursor()
    #     try:
    #         cur.execute("UPDATE line_message SET update_flg = '" + str(cls_epever_control_common.update_flg_linemsg_off) + "', send_datetime = '" + send_datetime + "' WHERE number = " + str(number))
    #         conn.commit()
    #         ret = self.lvNormal
    #     except sqlite3.Error as e:
    #         print(e)
    #         ret = self.lvError

    #     conn.close()
    #     return ret



class epever_control_tool:
    def __init__(self):
        cls_epever_control_common = epever_control_commonvalue()
        self.lvNormal = cls_epever_control_common.lvNormal
        self.lvError = cls_epever_control_common.lvError

    def to_numericval_unit(self, strr):
        exvalue = strr.split('=', 1)[1] #extract value
        m = re.findall(r'\d+', exvalue)
        mlen = len(m)
        exvaluelen = len(exvalue)
        if mlen == 2:
            numericval = m[0] + '.' + m[1]
            numericlen = len(m[0]) + 1 + len(m[1])
        elif mlen == 1:
            numericval = m[0]
            numericlen = len(m[0])
        elif mlen == 0:
            numericval = '-'
            numericlen = 1
        
        self.to_numericval = numericval
        self.to_unit = exvalue[numericlen + 1:]

        
#this module test
#You can test epever_control_setting.py in command line console.
def Test():
    cls_epever_control_commonvalue = epever_control_commonvalue()

    cls_epever_control_db = epever_control_db()
    print('dbPath = ' + cls_epever_control_db.dbPath)
    if cls_epever_control_db.read_control_nums(cls_epever_control_db.dbPath) == cls_epever_control_db.lvNormal:
        for num in cls_epever_control_db.numlist:
            print("table [control]******************")
            print('ctrlNum = ' + str(num[0]))
            print('read_control = ' + str(cls_epever_control_db.read_control(cls_epever_control_db.dbPath, num[0])))
            print('read_control_Vmax = ' + str(cls_epever_control_db.Vmax))
            print('read_control_Vmin = ' + str(cls_epever_control_db.Vmin))
            print('read_control_Starttime = ' + str(cls_epever_control_db.Startime))
            print('read_control_Endtime = ' + str(cls_epever_control_db.Endtime))
            print('read_control_Relay1 = ' + cls_epever_control_db.Relay1)
            print('read_control_Relay2 = ' + cls_epever_control_db.Relay2)
            print('read_control_Relay3 = ' + cls_epever_control_db.Relay3)

    if cls_epever_control_db.read_colname(cls_epever_control_db.dbPath) == cls_epever_control_commonvalue.lvNormal:
        print("epever parameters******************")
        for lst in cls_epever_control_db.lstColname:
            print(lst)

    cls_epever_control_tool = epever_control_tool()
    strr = "Charging equipment input current = 27.15V"
    print(strr)
    result = cls_epever_control_tool.to_numericval_unit(strr)
    print(cls_epever_control_tool.to_numericval)
    print(cls_epever_control_tool.to_unit)
    strr = "Charging equipment input current = 999.99ABCD"
    print(strr)
    result = cls_epever_control_tool.to_numericval_unit(strr)
    print(cls_epever_control_tool.to_numericval)
    print(cls_epever_control_tool.to_unit)

    # result = cls_epever_control_db.read_line_message_maxnumber(cls_epever_control_db.line_message_dbPath)
    # print(cls_epever_control_db.line_message_maxnumber + 1)
    # cls_epever_control_db.write_line_message(cls_epever_control_db.line_message_dbPath, cls_epever_control_commonvalue.update_flg_linemsg_on, '2021/08/29 22:15:00', '2021/08/29 22:15:00', 'test', cls_epever_control_db.line_message_maxnumber + 1)

    # print("LINE Messaging API settings")
    # print(cls_epever_control_db.line_message_enable)
    # print(cls_epever_control_db.line_message_dbPath)

if __name__ == '__main__':
    Test()