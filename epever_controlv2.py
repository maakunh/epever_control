#epever_controlv2.py
#epever control ver 2.0 Update: 26/08/2021
#Author: Masafumi Hiura
#URL: https://github.com/maakunh/epever_control
#This code watch output voltage of Charge Controllers, and control on/off of relays conected Inverters(GTI etc). 
#You write your environment parameters in epever_control_setting.py
#This code needs additional codes below...
#->relaywrite.py
#->relayread.py
#For download above codes, access to url below...
#https://github.com/maakunh/numato_usb_relay

#This code needs 3 products below...
#->Epever Charge Controller
## https://www.epsolarpv.com/productlist_1_7.html
#->Numato Lab USB relay module
## https://numato.com/product-category/automation/relay-modules/usb-relay/
#->USB to RS485 adapter
## https://www.google.com/search?q=USB+to+RS485+adapter
## I use products below.
### DSD TECH SH-U08A
### DSD TECH SH-U11
### Additional Information ###
### You can make RJ45 cable(ethernet cable) for connect your PC to Epever Charge Controller.
### Refer to urls below.
### https://github.com/tekk/Tracer-RS485-Modbus-Blynk-V2
### https://github.com/tekk/Tracer-RS485-Modbus-Blynk-V2/blob/master/doc/1733_modbus_protocol.pdf
#
#This code needs external codes below...
#->pyepsolartracer
## https://github.com/kasbert/epsolar-tracer
#->pymodbus
## https://github.com/riptideio/pymodbus
#->pyserial
## https://github.com/pyserial/pyserial
#->six
## https://github.com/benjaminp/six


import time
import datetime
import sys
import sqlite3
import subprocess
import epever_control_setting

if (len(sys.argv) < 1):
	print("Usage: epever_controlvx.py <control number>")
	sys.exit(0)
else:
	ctrlNum = sys.argv[1]

#setting
portNames = epever_control_setting.epever_control_portName()
baudRate = int(epever_control_setting.epever_control_ccbaudrate())
dbPath = epever_control_setting.epever_control_dbpath()
numato_portName = epever_control_setting.numato_portName()
numato_baudrate = epever_control_setting.numato_baudrate()
numato_relaywrite_py = epever_control_setting.numato_relaywrite_py()
numato_relayread_py = epever_control_setting.numato_relayread_py()

# import EPsolarTracerClient
from pyepsolartracer.client import EPsolarTracerClient
from pyepsolartracer.registers import registers,coils
# import the server implementation
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.mei_message import *
from pyepsolartracer.registers import registers,coils
import serial.rs485

lvalue = list() #history data
# datetime
dt_now = datetime.datetime.now()
lvalue.append(dt_now.strftime('%Y/%m/%d %H:%M:%S')) #history data
lvalue.append(ctrlNum) #history data

# initialize CC data
valV = 0.0
valC = 0.0
iCount = 0
# the serial client connection
for portName in portNames:
    print(portName)
    serialclient = ModbusClient(method ='rtu', port = portName, baudrate = baudRate, stopbits = 1, bytesize = 8, timeout=1)
    client = EPsolarTracerClient(serialclient = serialclient)
    client.connect()

    # response from Charge Controller
    # "Charging equipment output voltage"
    response = client.read_input("Charging equipment output voltage")
    strr = str(response)
    valV = valV + float(strr.split('=', 1)[1].strip()[:-1]) #extract value
    # "Charging equipment output current"
    response = client.read_input("Charging equipment output current")
    strr = str(response)
    valC = valC + float(strr.split('=', 1)[1].strip()[:-1]) #extract value

    client.close() #end serial connection
    iCount = iCount + 1
valV = valV / iCount    #average of cc output voltage
lvalue.append(valV) #history data
lvalue.append(valC) #history data

# database connection
dbname = dbPath
print(dbname)
conn = sqlite3.connect(dbname)
cur = conn.cursor()

try:
    cur.execute("SELECT * FROM control WHERE num =" + ctrlNum)
    ctrllist = cur.fetchone()
except sqlite3.Error as e:
    print(e)
    sys.exit(0)
    
Vmax = float(ctrllist[1])
Vmin = float(ctrllist[2])
Starttime = datetime.datetime(year=int(dt_now.strftime('%Y')), month=int(dt_now.strftime('%m')), day=int(dt_now.strftime('%d')), hour=int(ctrllist[3].strip()[:2]),  minute=int(ctrllist[3].strip()[2:]))
Endtime = Starttime + datetime.timedelta(hours=int(ctrllist[4][:2]),  minutes=int(ctrllist[4][2:]))
Relay1 = ctrllist[5]
Relay2 = ctrllist[6]
Relay3 = ctrllist[7]

print('Process start from ' + str(Starttime))
print ('Process end to ' + str(Endtime))

#GTI ON
if dt_now > Starttime:
    if dt_now < Endtime: #Process Running
        if valV > Vmax:
            result = subprocess.run('py.exe ' + numato_relayread_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay1, shell=True, stdout = subprocess.PIPE)
            relay_status1 = result.stdout.decode().replace('\r\n','')
            if relay_status1 == "off":
                result = subprocess.run('py.exe ' + numato_relaywrite_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay1 + ' on', shell=True)
                lvalue.append('relay' + Relay1 + '　on dt_time>Startime dt_time<Endtime valV>Vmax control start relay1') #history data1:2
            elif relay_status1 == "on":
                    result = subprocess.run('py.exe ' + numato_relayread_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay2, shell=True, stdout = subprocess.PIPE)
                    relay_status2 = result.stdout.decode().replace('\r\n','')
                    if relay_status2 == "off":
                        result = subprocess.run('py.exe ' + numato_relaywrite_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay2 + ' on', shell=True)
                        lvalue.append('relay' + Relay2 + '　on dt_time>Startime dt_time<Endtime valV>Vmax control start relay2') #history data1:2
                    elif relay_status2 == "on":
                        result = subprocess.run('py.exe ' + numato_relayread_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay3, shell=True, stdout = subprocess.PIPE)
                        relay_status3 = result.stdout.decode().replace('\r\n','')
                        if relay_status3 == "off":
                            result = subprocess.run('py.exe ' + numato_relaywrite_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay3 + ' on', shell=True)
                            lvalue.append('relay' + Relay3 + '　on dt_time>Startime dt_time<Endtime valV>Vmax control start relay3') #history data1:2
                        elif relay_status3 == "on":
                            lvalue.append('relay full on dt_time>Startime dt_time<Endtime valV>Vmax control full ') #history data1:2
        elif valV < Vmin:
            result = subprocess.run('py.exe ' + numato_relayread_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay3, shell=True, stdout = subprocess.PIPE)
            relay_status3 = result.stdout.decode().replace('\r\n','')
            if relay_status3 == "on":
                result = subprocess.run('py.exe ' + numato_relaywrite_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay3 + ' off', shell=True)
                lvalue.append('relay' + Relay3 + '　off dt_time>Startime dt_time<Endtime valV<Vmin control temporary stop(voltage lower limit)') #history data1:2
            elif relay_status3 == "off":
                    result = subprocess.run('py.exe ' + numato_relayread_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay2, shell=True, stdout = subprocess.PIPE)
                    relay_status2 = result.stdout.decode().replace('\r\n','')
                    if relay_status2 == "on":
                        result = subprocess.run('py.exe ' + numato_relaywrite_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay2 + ' off', shell=True)
                        lvalue.append('relay' + Relay2 + '　on dt_time>Startime dt_time<Endtime valV<Vmin control temporary stop(voltage lower limit)') #history data1:2
                    elif relay_status2 == "off":
                        result = subprocess.run('py.exe ' + numato_relayread_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay1, shell=True, stdout = subprocess.PIPE)
                        relay_status1 = result.stdout.decode().replace('\r\n','')
                        if relay_status1 == "on":
                            result = subprocess.run('py.exe ' + numato_relaywrite_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay1 + ' off', shell=True)
                            lvalue.append('relay' + Relay1 + '　on dt_time>Startime dt_time<Endtime valV<Vmin control temporary stop(voltage lower limit)') #history data1:2
                        elif relay_status1 == "off":
                            lvalue.append('relay all off dt_time>Startime dt_time<Endtime valV<Vmin not control') #history data
        else:
            lvalue.append('dt_time>Startime dt_time<Endtime Vmin<valV<Valmax') #history data
#GTI OFF
    elif dt_now > Endtime: #Process End              
            result = subprocess.run('py.exe ' + numato_relayread_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay3, shell=True, stdout = subprocess.PIPE)
            print('py.exe ' + numato_relayread_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay3)
            relay_status3 = result.stdout.decode().replace('\r\n','')
            print(relay_status3)
            if relay_status3 == "on":
                result = subprocess.run('py.exe ' + numato_relaywrite_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay3 + ' off', shell=True)
                lvalue.append('relay' + Relay3 + ' off dt_time>Startime dt_time>Endtime process end(time over)') #history data
            elif relay_status3 == "off":
                    result = subprocess.run('py.exe ' + numato_relayread_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay2, shell=True, stdout = subprocess.PIPE)
                    relay_status2 = result.stdout.decode().replace('\r\n','')
                    print(relay_status2)
                    if relay_status2 == "on":
                        result = subprocess.run('py.exe ' + numato_relaywrite_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay2 + ' off', shell=True)
                        lvalue.append('relay' + Relay2 + ' off dt_time>Startime dt_time>Endtime process end(time over)') #history data
                    elif relay_status2 == "off":
                        result = subprocess.run('py.exe ' + numato_relayread_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay1, shell=True, stdout = subprocess.PIPE)
                        relay_status1 = result.stdout.decode().replace('\r\n','')
                        print(relay_status1)
                        if relay_status1 == "on":
                            result = subprocess.run('py.exe ' + numato_relaywrite_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay1 + ' off', shell=True)
                            lvalue.append('relay' + Relay1 + ' off dt_time>Startime dt_time>Endtime process end(time over)') #history data
                        elif relay_status1 == "off":
                            lvalue.append('relay all off dt_time>Startime dt_time>Endtime process end(time over)') #history data
    elif dt_now == Endtime:
        lvalue.append('dt_now=Endtime else') #history data
#GTI OFF
elif dt_now < Starttime: #before process start
    lvalue.append('dt_time<Starttime dttime<Endtime before process start') #history data
elif dt_now == Starttime:
    lvalue.append('dt_now=Starttime else') #history data

print(lvalue)

try:
    cur.execute("INSERT INTO control_history VALUES(?, ?, ?, ?, ?)", lvalue)
    conn.commit()
except sqlite3.Error as e:
    print(e)
 
conn.close()


