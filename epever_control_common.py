#epever_control_common.py
#epever control ver 2.0 Update: 27/08/2021
#Author: Masafumi Hiura
#URL: https://github.com/maakunh/epever_control
#This code is the common parameter/function of epever_control 

import datetime
import time
import sqlite3
import epever_control_setting


class epever_control_db:
    def __init__(self):
        self.lvNormal = 0
        self.lvError = 1
        self.dbPath = epever_control_setting.epever_control_dbpath()
        self.dt_now = datetime.datetime.now()

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
            self.ctrllist = cur.fetchone()
            ret = self.lvNormal
        except sqlite3.Error as e:
            print(e)
            ret = self.lvError
    
        conn.close()

        #set result values
        self.Vmax = float(self.ctrllist[1])
        self.Vmin = float(self.ctrllist[2])
        self.Startime = datetime.datetime(year=int(self.dt_now.strftime('%Y')), month=int(self.dt_now.strftime('%m')), day=int(self.dt_now.strftime('%d')), hour=int(self.ctrllist[3].strip()[:2]),  minute=int(self.ctrllist[3].strip()[2:]))
        self.Endtime = self.Startime + datetime.timedelta(hours=int(self.ctrllist[4][:2]),  minutes=int(self.ctrllist[4][2:]))
        self.Relay1 = self.ctrllist[5]
        self.Relay2 = self.ctrllist[6]
        self.Relay3 = self.ctrllist[7]
    
        return ret


#this module test
#You can test epever_control_setting.py in command line console.
def Test():
    cls_epever_control_db = epever_control_db()
    print('dbPath = ' + cls_epever_control_db.dbPath)
    if cls_epever_control_db.read_control_nums(cls_epever_control_db.dbPath) == cls_epever_control_db.lvNormal:
        for num in cls_epever_control_db.numlist:
            print('ctrlNum = ' + str(num[0]))
            print('read_control = ' + str(cls_epever_control_db.read_control(cls_epever_control_db.dbPath, num[0])))
            print('read_control_Vmax = ' + str(cls_epever_control_db.Vmax))
            print('read_control_Vmin = ' + str(cls_epever_control_db.Vmin))
            print('read_control_Starttime = ' + str(cls_epever_control_db.Startime))
            print('read_control_Endtime = ' + str(cls_epever_control_db.Endtime))
            print('read_control_Relay1 = ' + cls_epever_control_db.Relay1)
            print('read_control_Relay2 = ' + cls_epever_control_db.Relay2)
            print('read_control_Relay3 = ' + cls_epever_control_db.Relay3)
if __name__ == '__main__':
    Test()