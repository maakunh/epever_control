#epever_control_setting.py
#epever control ver 2.0 Update: 26/08/2021
#Author: Masafumi Hiura
#URL: https://github.com/maakunh/epever_control
#This code is imported by epever_controlvx.py.
#You write your environment parameters in this code.
#These parameters below are samples.

#subprocess return code in stdout
def epever_control_stdout_rtncode():
    return '\n'
    #if your os is windows...
    #return '\r\n'

#epever_control setting
def epever_control_python():
    return 'python3'
    
#MySQL Connection------------------
def epever_control_db_unix_socket():
    return '' # if you need unix socket, write this parameter.

def epever_control_db_user():
    return 'your db user'

def epever_control_db_passwd():
    return 'your db password'

def epever_control_db_host():
    return 'your db ip/hostname'

def epever_control_db_db():
    return 'your db name'
#------------------MySQL Connection

def epever_control_portName(): #muliple Charge Controllers allow
    return '/dev/ttyUSB0', '/dev/ttyUSB1' #port name connected to CC.

def epever_control_ccbaudrate():
    return '115200'

#numato lab usb relay setting

def numato_portName():
    return '/dev/ttyACM0'   #port name connnected to numato USB Relay

def numato_relayNum():
    return '8'  #this example is for URMC8

def numato_baudrate():
    return '9600'

def numato_relaywrite_py():
    return '/home/user01/apps/numato_usb_relay_mysql/relaywrite.py'

def numato_relayread_py():
    return '/home/user01/apps/numato_usb_relay_mysql/relayread.py'


#LINE Messaging API
def update_flg_linemsg_on():
    return 2

def update_flg_linemsg_off():
    return 9

def update_flg_linemsg_ignore():
    return 99

def line_message_enable():
    return True #If you don't use LINE Messaging API, change False

def line_message_py():
    return '/home/user01/apps/LINE_Messaging_API_mysql/line_message.py'

def line_message_application():
    return 'epever_control'

#retry mesurement
def retry(req_name): #if value < retry_volt then retry mesurement
    if req_name == "Charging equipment output voltage":
        return float(24.0)
    elif req_name == "Charging equipment input voltage":
        return float(52.0)
    else:
        return float(-2000.0)

def retry_upper(req_name): #if value < retry_volt then retry mesurement
    if req_name == "Charging equipment output voltage":
        return float(31.1)
    elif req_name == "Charging equipment input voltage":
        return float(62.2)
    elif req_name == "Charging equipment input current":
        return float(15.6)
    elif req_name == "Charging equipment output current":
        return float(31.1)
    else:
        return float(2000.0)


def retry_count(): #how many times retry
    return 5

def retry_duration(): # retry duration sec
    return 3

def retry_diff(): # retry duration sec
    return 8.0


# duration(min) of excecuting epever_control_watchvc_mysql.py
def duration_min():
    return 3


#this module test
#You can test epever_control_setting.py in command line console.
def test():
    print('epever_control_portName = ')
    print(epever_control_portName())
    print('epever_control_ccbaudrate = ' + epever_control_ccbaudrate())
    print('numato_portName = ' + numato_portName())
    print('numato_relayNum = ' + numato_relayNum())
    print('numato_baudrate = ' + numato_baudrate())
if __name__ == '__main__':
    test()