#database setting
def db_unix_socket():
    return ''

def db_user():
    return 'your db user'

def db_passwd():
    return 'your db password'

def db_host():
    return 'your db ip/hostname'

def db_db():
    return 'your db name'

#Serial Port
def epever_control_portName(): #muliple Charge Controllers allow
    return '/dev/ttyUSB0', '/dev/ttyUSB1' #port name connected to CC.

#tariff /1kwh
def tariff():
    return '21.04'

def tariff_unit():
    return 'Yen'

#Threshold of your PV system
#Input Power
def ip_err_under():
    return float(270.0)
def ip_err_upper():
    return float(2500.0)
#Input Voltage
def iv_err_under():
    return float(40.0)
def iv_err_upper():
    return float(72.58)
#Input Cuurent
def ic_err_under():
    return float(1.8)
def ic_err_upper():
    return float(50.0)

#Output Power
def op_err_under():
    return float(270.0)
def op_err_upper():
    return float(2500.0)
#Output Voltage
def ov_err_under():
    return float(26.05)
def ov_err_upper():
    return float(29.2)
#Output Cuurent
def oc_err_under():
    return float(3.5)
def oc_err_upper():
    return float(100.0)

def epever_control_python():
    return 'python3'
def line_message_py():
    return '/home/user01/apps/LINE_Messaging_API_mysql/line_message.py'
def line_message_application():
    return 'epever_control'
