#webapp_common.py

import mysql.connector as MySQLdb
import re
import time
import sys
import glob
import subprocess
import serial

from . import webapp_setting

class webapp_commonvalue:
     def __init__(self):
        self.lvNormal = 0
        self.lvError = 1
        self.lvAlert = 8
        self.flgon = 2
        self.flgoff = 9
        self.flgignore = 99
        self.notfound = 999

class webapp_validation:
    def __init__(self):
        self.lvNormal = 0
        self.lvError = 1

    def num(self, num):
        pattern = re.compile('^[0-9]+')
        if pattern.fullmatch(str(num)):
            return self.lvNormal
        else:
            return self.lvError

    def voltage(self, voltage):
        pattern = re.compile('^[0-9]+\.[0-9]+')
        if pattern.fullmatch(voltage):
            return self.lvNormal
        else:
            return self.lvError

    def starttime(self, starttime):
        if int(starttime[:2]) < 24:
            pattern = re.compile('^[0-2][0-9][0-5][0-9]')
            if pattern.fullmatch(starttime):
                return self.lvNormal
            else:
                return self.lvError
        else:
            return self.lvError

    def duration(self, duration):
        pattern = re.compile('^[0-9]{4}')
        if pattern.fullmatch(duration):
            return self.lvNormal
        else:
            return self.lvError

    def relay(self, relay):
        pattern = re.compile('^[0-9]+')
        if pattern.fullmatch(relay):
            return self.lvNormal
        else:
            return self.lvError

class webapp_db:
    def __init__(self):
        self.db_unix_socket = webapp_setting.db_unix_socket()
        self.db_user = webapp_setting.db_user()
        self.db_passwd = webapp_setting.db_passwd()
        self.db_host = webapp_setting.db_host()
        self.db_db = webapp_setting.db_db()
        cls = webapp_commonvalue()
        self.lvNormal = cls.lvNormal
        self.lvError = cls.lvError
        self.flgon = cls.flgon
        self.flgoff = cls.flgoff
        self.flgignore = cls.flgignore
    
    def read_record_simple(self):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM record_simple ORDER BY datetime DESC LIMIT 12960")
            print("SELECT * FROM record_simple ORDER BY datetime DESC LIMIT 12960")
            self.read_db_list = cur.fetchall()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError
    
        conn.close()
        return ret

    def read_record_simple_key(self, port, date):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT datetime, ivoltage, icurrent, ovoltage, ocurrent FROM record_simple WHERE port = '" + port + "' AND datetime like '" + date + "%' ORDER BY datetime DESC")
            print("SELECT datetime, ivoltage, icurrent, ovoltage, ocurrent FROM record_simple WHERE port = '" + port + "' AND datetime like '" + date + "%' ORDER BY datetime DESC")
            self.read_db_list = cur.fetchall()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError
    
        conn.close()
        return ret

    def read_record_simple_ivoltage_key(self, port, date):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT datetime, ivoltage FROM record_simple WHERE port = '" + port + "' AND datetime like '" + date + "%'")
            print("SELECT datetime, ivoltage FROM record_simple WHERE port = '" + port + "' AND datetime like '" + date + "%'")
            self.read_db_list = cur.fetchall()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError
    
        conn.close()
        return ret

    def read_record_simple_icurrent_key(self, port, date):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT datetime, icurrent FROM record_simple WHERE port = '" + port + "' AND datetime like '" + date + "%'")
            print("SELECT datetime, icurrent FROM record_simple WHERE port = '" + port + "' AND datetime like '" + date + "%'")
            self.read_db_list = cur.fetchall()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError
    
        conn.close()
        return ret

    def read_record_simple_ovoltage_key(self, port, date):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT datetime, ovoltage FROM record_simple WHERE port = '" + port + "' AND datetime like '" + date + "%'")
            print("SELECT datetime, ovoltage FROM record_simple WHERE port = '" + port + "' AND datetime like '" + date + "%'")
            self.read_db_list = cur.fetchall()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError
    
        conn.close()
        return ret

    def read_record_simple_ocurrent_key(self, port, date):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT datetime, ocurrent FROM record_simple WHERE port = '" + port + "' AND datetime like '" + date + "%'")
            print("SELECT datetime, ocurrent FROM record_simple WHERE port = '" + port + "' AND datetime like '" + date + "%'")
            self.read_db_list = cur.fetchall()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError
    
        conn.close()
        return ret

    def count_record_simple_key(self, port, date):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT COUNT(*) FROM record_simple WHERE port = '" + port + "' AND datetime like '" + date + "%'")
            print("SELECT COUNT(*) FROM record_simple WHERE port = '" + port + "' AND datetime like '" + date + "%'")
            self.read_db_list = cur.fetchone()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError
    
        conn.close()
        return ret

    def read_recordall(self):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM recordall ORDER BY datetime DESC LIMIT 1440")
            print("SELECT * FROM recordall ORDER BY datetime DESC LIMIT 1440")
            self.read_db_list = cur.fetchall()
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
            self.read_db_list = cur.fetchone()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

    def read_control_history(self):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM control_history ORDER BY datetime DESC LIMIT 12960")
            print("SELECT * FROM control_history ORDER BY datetime DESC LIMIT 12960")
            self.read_db_list = cur.fetchall()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

    def read_power_result_key(self, datehour):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM power_result WHERE dateh like '" + datehour + "%'")
            print("SELECT * FROM power_result WHERE dateh like '" + datehour + "%'")
            self.recordlist = cur.fetchall()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

    def count_power_result_key(self, datehour):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT COUNT(*) FROM power_result WHERE dateh like '" + datehour + "%'")
            print("SELECT COUNT(*) FROM power_result WHERE dateh like '" + datehour + "%'")
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
            cur.execute("SELECT SUM(ikwh) FROM power_result WHERE dateh like '" + date + "%'")
            print("SELECT SUM(ikwh) FROM power_result WHERE dateh like '" + date + "%'")
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
            cur.execute("SELECT SUM(okwh) FROM power_result WHERE dateh like '" + date + "%'")
            print("SELECT SUM(okwh) FROM power_result WHERE dateh like '" + date + "%'")
            self.recordlist = cur.fetchone()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

    def read_control(self):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM control")
            print("SELECT * FROM control")
            self.read_db_list = cur.fetchall()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

    def count_control(self):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT COUNT(*) FROM control")
            print("SELECT COUNT(*) FROM control")
            self.read_db_list = cur.fetchone()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

    def update_control(self):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("UPDATE control SET voltage_max = '" + self.voltage_max + "', voltage_min = '" + self.voltage_min + "', starttime = '" + self.starttime + "', duration = '" + self.duration + "', relay1 ='" + self.relay1 + "', relay2 = '" + self.relay2 + "', relay3 = '" + self.relay3 + "' WHERE num = " + str(self.num))
            print("UPDATE control SET voltage_max = '" + self.voltage_max + "', voltage_min = '" + self.voltage_min + "', starttime = '" + self.starttime + "', duration = '" + self.duration + "', relay1 ='" + self.relay1 + "', relay2 = '" + self.relay2 + "', relay3 = '" + self.relay3 + "' WHERE num = " + str(self.num))
            conn.commit()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

    def write_control(self, lvalue):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            print("INSERT INTO control VALUES(%s, %s, %s, %s, %s, %s, %s, %s)")
            print(lvalue)
            cur.execute("INSERT INTO control VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", lvalue)
            conn.commit()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

    def delete_control(self, num):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            print("DELETE FROM control WHERE num = '" + str(num) + "'")
            cur.execute("DELETE FROM control WHERE num = '" + str(num) + "'")
            conn.commit()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

    def max_num_control(self):
        if(self.db_unix_socket != ''):
            conn = MySQLdb.connect(unix_socket=self.db_unix_socket, user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        else:
            conn = MySQLdb.connect(user=self.db_user, passwd=self.db_passwd, host=self.db_host, database=self.db_db)
        cur = conn.cursor()

        try:
            cur.execute("SELECT MAX(num) from control")
            print("SELECT MAX(num) from control")
            self.read_db_list = cur.fetchone()
            ret = self.lvNormal
        except MySQLdb.Error as e:
            print(e)
            ret = self.lvError

        conn.close()
        return ret

class webapp_tool:
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

    def server_restart(self):
        self.line_message("restart server. epever_control_common: epever_control_tool: server_restart")
        #if you use this method, execute "sudo visudo" and add your user information to definitions.
        cmd = "sudo init 6"
        print(cmd)
        subprocess.run(cmd, shell=True)

    def line_message(self, linemsg_msg):
        py = webapp_setting.epever_control_python()
        linemsg_py = webapp_setting.line_message_py()
        linemsg_application = webapp_setting.line_message_application()
        result = subprocess.run(py + ' ' + linemsg_py + ' r ' + ' "' + linemsg_msg + '" "' + linemsg_application + '"', shell=True)
        return result
