#epever_control_setting.py
#epever control ver 2.0 Update: 26/08/2021
#Author: Masafumi Hiura
#URL: https://github.com/maakunh/epever_control
#This code is imported by epever_controlvx.py.
#You write your environment parameters in this code.
#These parameters below are samples.

#epever_control setting
def epever_control_dbpath():
    return r'\\DESKTOP-2322PPH\Users\Public\epever\epever.db'

def epever_control_portName(): #muliple Charge Controllers allow
    return 'COM7', 'COM4'

def epever_control_ccbaudrate():
    return '115200'

#numato lab usb relay setting

def numato_relay_db():
    return r'\\DESKTOP-2322PPH\Users\Public\numato\numato.db'

def numato_portName():
    return 'COM3'

def numato_relayNum():
    return '8'

def numato_baudrate():
    return '9600'

def numato_relaywrite_py():
    return r'\\desktop-2322pph\Users\Public\numato\relaywrite.py'

def numato_relayread_py():
    return r'\\desktop-2322pph\Users\Public\numato\relayread.py'


#LINE Messaging API
def line_message_enable():
    return True #If you don't use LINE Messaging API, change False
def line_message_dbpath():
    return r'\\DESKTOP-2322PPH\Users\Public\line_message\linemessage.db'

#this module test
#You can test epever_control_setting.py in command line console.
def test():
    print('epever_control_dbpath = ' + epever_control_dbpath())
    print('epever_control_portName = ')
    print(epever_control_portName())
    print('epever_control_ccbaudrate = ' + epever_control_ccbaudrate())
    print('numato_relay_db = ' + numato_relay_db())
    print('numato_portName = ' + numato_portName())
    print('numato_relayNum = ' + numato_relayNum())
    print('numato_baudrate = ' + numato_baudrate())
if __name__ == '__main__':
    test()