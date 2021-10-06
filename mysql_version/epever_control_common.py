#epever_control_common.py
#epever control ver 2.0 Update: 27/08/2021
## Modified: 28/08/2021
#Author: Masafumi Hiura
#URL: https://github.com/maakunh/epever_control
#This code is the common parameter/function of epever_control 

import datetime
import time
import mysql.connector as MySQLdb
import re
import subprocess
import sys
import glob

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
        self.flgon = 2
        self.flgoff = 9
        self.flgignore = 99
        # self.update_flg_linemsg_on = 2
        # self.update_flg_linemsg_off = 9
        # self.update_flg_linemsg_ignore = 99
         
class epever_control_db:
    def __init__(self):
        cls_epever_control_common = epever_control_commonvalue()
        self.lvNormal = cls_epever_control_common.lvNormal
        self.lvError = cls_epever_control_common.lvError
        self.db_unix_socket = epever_control_setting.epever_control_db_unix_socket()
        self.db_user = epever_control_setting.epever_control_db_user()
        self.db_passwd = epever_control_setting.epever_control_db_passwd()
        self.db_host = epever_control_setting.epever_control_db_host()
        self.db_db = epever_control_setting.epever_control_db_db()
       

        self.dt_now = datetime.datetime.now()
        # self.line_message_enable = epever_control_setting.line_message_enable()
        # self.line_message_dbPath = epever_control_setting.line_message_dbpath()

    def read_control_nums(self):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()
        try:
            cur.execute("SELECT num FROM control")
            print("SELECT num FROM control")
            self.numlist = cur.fetchall()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError
        conn.close()
        return ret

    def read_control(self, ctrlNum):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM control WHERE num =" + str(ctrlNum))
            print("SELECT * FROM control WHERE num =" + str(ctrlNum))
            self.lstCtrl = cur.fetchone()
            ret = self.lvNormal
        except MySQLdb.Error as e:
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
    
    def write_control_history(self, lvalue):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO control_history VALUES(%s, %s, %s, %s, %s, %s)", lvalue)
            print("INSERT INTO control_history VALUES(%s, %s, %s, %s, %s, %s)")
            conn.commit()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret
    

    def read_record_simple(self):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM record_simple ORDER BY datetime DESC LIMIT 1440")
            print("SELECT * FROM record_simple ORDER BY datetime DESC LIMIT 1440")
            self.recordlist = cur.fetchall()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError
    
        conn.close()
        return ret

    def write_record_simple(self, lvalue):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO record_simple VALUES(%s, %s, %s, %s, %s, %s)", lvalue)
            print("INSERT INTO record_simple VALUES(%s, %s, %s, %s, %s, %s)")
            conn.commit()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

    def read_record_key(self, port, datetime_key):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT datetime, ivoltage, icurrent, ovoltage, ocurrent FROM record_simple WHERE port = 'ALL' AND datetime like '" + datetime_key + "%'")
            print("SELECT datetime, ivoltage, icurrent, ovoltage, ocurrent FROM record_simple WHERE port = 'ALL' AND datetime like '" + datetime_key + "%'")
            self.recordlist = cur.fetchall()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

    def count_record_key(self, port, datetime_key):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT COUNT(*) FROM record_simple WHERE port = 'ALL' AND datetime like '" + datetime_key + "%'")
            print("SELECT COUNT(*) FROM record_simple WHERE port = 'ALL' AND datetime like '" + datetime_key + "%'")
            self.recordlist = cur.fetchone()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

    def write_power_result(self, lvalue):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO power_result VALUES(%s, %s, %s)", lvalue)
            print("INSERT INTO power_result VALUES(%s, %s, %s)")
            conn.commit()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

    def update_power_result(self, datehour, ikwh, okwh):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("UPDATE power_result SET ikwh = '" + ikwh + "', okwh = '" + okwh + "' WHERE dateh = '" + datehour + "'")
            print("UPDATE power_result SET ikwh = '" + ikwh + "', okwh = '" + okwh + "' WHERE dateh = '" + datehour + "'")
            conn.commit()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

    def count_power_result(self, datehour):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT COUNT(*) FROM power_result WHERE dateh = '" + datehour + "'")
            print("SELECT COUNT(*) FROM power_result WHERE dateh = '" + datehour + "'")
            self.recordlist = cur.fetchone()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

    def read_power_result(self, datehour):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT ikwh, okwh FROM power_result WHERE dateh = '" + datehour + "'")
            print("SELECT ikwh, okwh FROM power_result WHERE dateh = '" + datehour + "'")
            self.recordlist = cur.fetchone()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret
    
    def sum_power_result_ikwh(self, date):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT SUM(ikwh) FROM power_result WHERE dateh LIKE '" + date + "%'")
            print("SELECT SUM(ikwh) FROM power_result WHERE dateh LIKE '" + date + "%'")
            self.recordlist = cur.fetchone()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

    def sum_power_result_okwh(self, date):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT SUM(okwh) FROM power_result WHERE dateh LIKE '" + date + "%'")
            print("SELECT SUM(okwh) FROM power_result WHERE dateh LIKE '" + date + "%'")
            self.recordlist = cur.fetchone()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret


    def read_colname(self):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM colname")
            print("SELECT * FROM colname")
            self.lstColname = cur.fetchone()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError
        
        conn.close()
        return ret

    def write_recordall(self, lvalue):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO recordall VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", lvalue)
            print("INSERT INTO recordall VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", lvalue)
            conn.commit()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret
    



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

    def calc_power(self, dateh):
        cls_db = epever_control_db()
        self.ikwh = 0.0
        self.okwh = 0.0
        for min in range(60): #from 00-59
            strmin = str(min)
            if len(strmin) == 1:
                strmin = '0' + strmin
            ret = cls_db.count_record_key('ALL', dateh + ":" + strmin + ":")
            
            if ret == cls_db.lvNormal:
                print("count_record:" + str(cls_db.recordlist[0]))
                if cls_db.recordlist[0] > 0:
                    ret = cls_db.read_record_key('ALL', dateh + ":" + strmin + ":")
                    if ret == cls_db.lvNormal:
                        ret = self.lvNormal
                        for record in cls_db.recordlist:
                            print(dateh + ":" + strmin)
                            print(record[0])
                            print(record[1])
                            print(record[2])
                            print(record[3])
                            print(record[4])
                            self.ikwh = self.ikwh + float(record[1]) * float(record[2]) / 60 / 1000 * epever_control_setting.duration_min()
                            self.okwh = self.okwh + float(record[3]) * float(record[4]) / 60 / 1000 * epever_control_setting.duration_min()
                            print("ikwh= " + str(self.ikwh))
                            print("okwh= " + str(self.okwh))
                    else:
                        ret = self.lvError
                else:
                    ret = self.lvNormal
                    self.ikwh = self.ikwh + 0.0
                    self.okwh = self.okwh + 0.0
            else:
                ret = self.lvError
  
        return ret

    def retry_mesurement(self, client, req_name):
        ic = 0
        while ic < epever_control_setting.retry_count():
            try:
                #get value from CC
                strr = str(client.read_input(req_name))
                print(strr)
                self.to_numericval_unit(strr)
                val = float(self.to_numericval)
                #evaluate value
                if val < epever_control_setting.retry(req_name):
                    #retry
                    print("retry: " + str(ic + 1))
                    time.sleep(epever_control_setting.retry_duration())
                else:
                    break
            except TypeError as e:
                print(e)
                val = 0.0
                pass
            except ValueError as e:
                print(e)
                val = 0.0
                pass

            ic = ic + 1

        ic = 0
        while ic < epever_control_setting.retry_count():
            try:
                #evaluate value that got above.
                if val > epever_control_setting.retry_upper(req_name):
                    strr = str(client.read_input(req_name))
                    print(strr)
                    self.to_numericval_unit(strr)
                    val = float(self.to_numericval)
                    print("retry: " + str(ic + 1))
                    time.sleep(epever_control_setting.retry_duration())
                else:
                    break
            except TypeError as e:
                print(e)
                pass
            except ValueError as e:
                print(e)
                pass

            ic = ic + 1

        return val

    def retry_mesurement2(self, client, req_name):
        ic = 0
        vallist = list()
        while ic < epever_control_setting.retry_count():
            try:
                #get value from CC
                strr = str(client.read_input(req_name))
                print(strr)
                self.to_numericval_unit(strr)
                vallist.append(float(self.to_numericval))
                print("retry: " + str(ic))
                time.sleep(epever_control_setting.retry_duration())
            except Exception as e:
                print(e)
                vallist.append(0.0)
                pass

            ic = ic + 1

        val_0 = 0.0
        diff = list()
        for val in vallist:
            diff.append(abs(val - val_0))
            val_0 = val

        val_sum = list()
        for i in range(ic):
            if diff[i] < epever_control_setting.retry_diff():
                val_sum.append(vallist[i])

        if float(len(val_sum)) == 0.0:
            val = 0.0
        else:
            val = sum(val_sum) / float(len(val_sum))

        return val


    def server_restart(self):
        self.line_message("restart server. epever_control_common: epever_control_tool: server_restart")
        #if you use this method, execute "sudo visudo" and add your user information to definitions.
        cmd = "sudo init 6"
        print(cmd)
        subprocess.run(cmd, shell=True)

    def line_message(self, linemsg_msg):
        py = epever_control_setting.epever_control_python()
        linemsg_py = epever_control_setting.line_message_py()
        linemsg_application = epever_control_setting.line_message_application()
        result = subprocess.run(py + ' ' + linemsg_py + ' r ' + ' "' + linemsg_msg + '" "' + linemsg_application + '"', shell=True)
        return result

    def active_serial_ports(self):
        if sys.platform.startswith('win'):
            #Window case, the module should appear in Windows Device Manager as a serial port(COMx).
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            #Linux case,"/dev/ttyUSBx"
            ports = glob.glob('/dev/ttyUSB*')
        elif sys.platform.startswith('darwin'):
            #Mac OS case,"/dev/cu.usbmodemx" or "/dev/tty.usbmodemx"
            ports = glob.glob('/dev/*.usb*')
        else:
            raise EnvironmentError('Unsupported platform')

        #Check serial connection, add only active port to list.
        result = list()
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                linemsg_msg = "Error from webapp_common: webapp_tool: active_serial_ports"
                print(linemsg_msg)
                self.line_message(linemsg_msg)
                self.server_restart()  # restart server
                pass

        return result

#this module test
#You can test epever_control_setting.py in command line console.
def Test():
    cls_epever_control_commonvalue = epever_control_commonvalue()

    cls_epever_control_db = epever_control_db()
    if cls_epever_control_db.read_control_nums() == cls_epever_control_db.lvNormal:
        for num in cls_epever_control_db.numlist:
            print("table [control]******************")
            print('ctrlNum = ' + str(num[0]))
            print('read_control = ' + str(cls_epever_control_db.read_control(num[0])))
            print('read_control_Vmax = ' + str(cls_epever_control_db.Vmax))
            print('read_control_Vmin = ' + str(cls_epever_control_db.Vmin))
            print('read_control_Starttime = ' + str(cls_epever_control_db.Startime))
            print('read_control_Endtime = ' + str(cls_epever_control_db.Endtime))
            print('read_control_Relay1 = ' + cls_epever_control_db.Relay1)
            print('read_control_Relay2 = ' + cls_epever_control_db.Relay2)
            print('read_control_Relay3 = ' + cls_epever_control_db.Relay3)

    if cls_epever_control_db.read_colname() == cls_epever_control_commonvalue.lvNormal:
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

    print(cls_epever_control_db.read_record_key('ALL', '2021/09/06 12'))
    print(cls_epever_control_db.recordlist)
    print(cls_epever_control_db.write_power_result(['2021090612', '3', '5']))
    print(cls_epever_control_db.read_power_result('2021090612'))
    print(cls_epever_control_db.recordlist)
    print(cls_epever_control_db.update_power_result('2021090612', '4', '6'))
    print(cls_epever_control_db.read_power_result('2021090612'))
    print(cls_epever_control_db.recordlist)
    print(cls_epever_control_db.count_power_result('2021090612'))
    print("count_power_result:" + str(cls_epever_control_db.recordlist[0]))
    print(cls_epever_control_db.sum_power_result_ikwh('2021090612'))
    print(cls_epever_control_db.recordlist)
    print(cls_epever_control_db.sum_power_result_okwh('2021090612'))
    print(cls_epever_control_db.recordlist)
    print(cls_epever_control_db.read_record_key('ALL', '2021/09/07 12'))
    print(cls_epever_control_db.recordlist)
    print(cls_epever_control_tool.calc_power("2021/09/07 12"))
    print(cls_epever_control_tool.ikwh)
    print(cls_epever_control_tool.ikwh)
   
if __name__ == '__main__':
    Test()