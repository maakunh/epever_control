#epever_controlv2.py
#############################################
#----new information----
#epever control ver 2.02 Update: 29/08/2021
##add LINE message request function by LINE Messaging API.
#----last information----
#epever control ver 2.01 Update: 27/08/2021
#epever control ver 2.0 Update: 26/08/2021
##create
#############################################
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


import datetime
import sys
import subprocess

#import original mudule
import epever_control_setting
import epever_control_common

#read common value
cls_epever_control_common_value = epever_control_common.epever_control_commonvalue()
lvNormal = cls_epever_control_common_value.lvNormal
lvError = cls_epever_control_common_value.lvError
flgon = cls_epever_control_common_value.flgon
flgoff = cls_epever_control_common_value.flgoff
flgignore = cls_epever_control_common_value.flgignore

if (len(sys.argv) < 1):
	print("Usage: epever_controlvx.py <control number>")
	sys.exit(0)
else:
    ctrlNum = sys.argv[1]
    linemsg_all = int(sys.argv[2])

#setting
py = epever_control_setting.epever_control_python()
portNames = epever_control_setting.epever_control_portName()
baudRate = int(epever_control_setting.epever_control_ccbaudrate())
dbPath = epever_control_setting.epever_control_dbpath()
numato_portName = epever_control_setting.numato_portName()
numato_baudrate = epever_control_setting.numato_baudrate()
numato_relaywrite_py = epever_control_setting.numato_relaywrite_py()
numato_relayread_py = epever_control_setting.numato_relayread_py()
linemsg_enable = epever_control_setting.line_message_enable()   #use or not use LINE Messaging API from this code
linemsg_py = epever_control_setting.line_message_py()
linemsg_dbpath = epever_control_setting.line_message_dbpath()
linemsg_application = epever_control_setting.line_message_application()

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
cls_epever_control_db = epever_control_common.epever_control_db()
ret = cls_epever_control_db.read_control(dbPath, ctrlNum)
if ret == lvNormal:
    Vmax = cls_epever_control_db.Vmax
    Vmin = cls_epever_control_db.Vmin
    Starttime = cls_epever_control_db.Startime
    Endtime = cls_epever_control_db.Endtime
    Relay1 = cls_epever_control_db.Relay1
    Relay2 = cls_epever_control_db.Relay2
    Relay3 = cls_epever_control_db.Relay3
elif ret == lvError:
    sys.exit(1)


print('Process start from ' + str(Starttime))
print ('Process end to ' + str(Endtime))


linemsg_update_flg = flgignore

#GTI ON
if dt_now > Starttime:
    if dt_now < Endtime: #Process Running
        if valV > Vmax:
            result = subprocess.run(py + ' ' + numato_relayread_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay1, shell=True, stdout = subprocess.PIPE)
            relay_status1 = result.stdout.decode().replace('\r\n','')
            if relay_status1 == "off":
                result = subprocess.run(py + ' ' + numato_relaywrite_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay1 + ' on', shell=True)
                lvalue.append('relay' + Relay1 + ' on dt_time>Startime dt_time<Endtime valV>Vmax control start 1st relay') #history data1:2
                linemsg_update_flg = flgon
                linemsg_msg = 'relay' + Relay1 + ' on \r\ncontrol start 1st relay\r\nVoltage = '+ str(valV) + '(>' + str(Vmax) + 'V) Current = ' + str(valC) + '\r\n'

            elif relay_status1 == "on":
                    result = subprocess.run(py + ' ' + numato_relayread_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay2, shell=True, stdout = subprocess.PIPE)
                    relay_status2 = result.stdout.decode().replace('\r\n','')
                    if relay_status2 == "off":
                        result = subprocess.run(py + ' ' + numato_relaywrite_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay2 + ' on', shell=True)
                        lvalue.append('relay' + Relay2 + ' on dt_time>Startime dt_time<Endtime valV>Vmax control start 2nd relay') #history data1:2
                        linemsg_update_flg = flgon
                        linemsg_msg = 'relay' + Relay2 + ' on \r\ncontrol start 2nd relay\r\nVoltage = ' + str(valV)  + '(>' + str(Vmax) + 'V) Current = ' + str(valC) + '\r\n'
                    elif relay_status2 == "on":
                        result = subprocess.run(py + ' ' + numato_relayread_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay3, shell=True, stdout = subprocess.PIPE)
                        relay_status3 = result.stdout.decode().replace('\r\n','')
                        if relay_status3 == "off":
                            result = subprocess.run(py + ' ' + numato_relaywrite_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay3 + ' on', shell=True)
                            lvalue.append('relay' + Relay3 + ' on dt_time>Startime dt_time<Endtime valV>Vmax control start 3rd relay') #history data1:2
                            linemsg_update_flg = flgon
                            linemsg_msg = 'relay' + Relay3 + ' on \r\ncontrol start 3rd relay\r\nVoltage = ' + str(valV) + '(>' + str(Vmax) + 'V) Current = ' + str(valC) + '\r\n'
                        elif relay_status3 == "on":
                            lvalue.append('relay full on dt_time>Startime dt_time<Endtime valV>Vmax control full ') #history data1:2
                            linemsg_update_flg = linemsg_all
                            linemsg_msg = 'relay full on dt_time>Startime dt_time<Endtime valV>Vmax control full '
        elif valV < Vmin:
            result = subprocess.run(py + ' ' + numato_relayread_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay3, shell=True, stdout = subprocess.PIPE)
            relay_status3 = result.stdout.decode().replace('\r\n','')
            if relay_status3 == "on":
                result = subprocess.run(py + ' ' + numato_relaywrite_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay3 + ' off', shell=True)
                lvalue.append('relay' + Relay3 + ' off dt_time>Startime dt_time<Endtime valV<Vmin 3rd relay temporary off(voltage lower limit)') #history data1:2
                linemsg_update_flg = flgon
                linemsg_msg = 'relay' + Relay3 + ' off \r\n3rd relay temporary off(voltage lower limit)\r\nVoltage = ' + str(valV) + '(<' + str(Vmin) + 'V) Current = ' + str(valC) + '\r\n'
            elif relay_status3 == "off":
                    result = subprocess.run(py + ' ' + numato_relayread_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay2, shell=True, stdout = subprocess.PIPE)
                    relay_status2 = result.stdout.decode().replace('\r\n','')
                    if relay_status2 == "on":
                        result = subprocess.run(py + ' ' + numato_relaywrite_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay2 + ' off', shell=True)
                        lvalue.append('relay' + Relay2 + ' off dt_time>Startime dt_time<Endtime valV<Vmin 2nd relay temporary stop(voltage lower limit)') #history data1:2
                        linemsg_update_flg = flgon
                        linemsg_msg = 'relay' + Relay2 + ' off \r\n2nd relay temporary stop(voltage lower limit)\r\nVoltage = ' + str(valV) + '(<' + str(Vmin) + 'V) Current = ' + str(valC) + '\r\n'
                    elif relay_status2 == "off":
                        result = subprocess.run(py + ' ' + numato_relayread_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay1, shell=True, stdout = subprocess.PIPE)
                        relay_status1 = result.stdout.decode().replace('\r\n','')
                        if relay_status1 == "on":
                            result = subprocess.run(py + ' ' + numato_relaywrite_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay1 + ' off', shell=True)
                            lvalue.append('relay' + Relay1 + ' off dt_time>Startime dt_time<Endtime valV<Vmin 1st relay temporary stop(voltage lower limit)') #history data1:2
                            linemsg_update_flg = flgon
                            linemsg_msg = 'relay' + Relay1 + ' off \r\n1st relay temporary stop(voltage lower limit)\r\nVoltage = ' + str(valV) + '(<' + str(Vmin) + 'V) Current = ' + str(valC) + '\r\n'
                        elif relay_status1 == "off":
                            lvalue.append('relay all off dt_time>Startime dt_time<Endtime valV<Vmin not control') #history data
                            linemsg_update_flg = linemsg_all
                            linemsg_msg = 'relay all off dt_time>Startime dt_time<Endtime valV<Vmin not control'
                            
            lvalue.append('dt_time>Startime dt_time<Endtime Vmin<valV<Valmax') #history data
            linemsg_update_flg = linemsg_all
            linemsg_msg = 'dt_time>Startime dt_time<Endtime Vmin<valV<Valmax'

#GTI OFF
    elif dt_now > Endtime: #Process End              
            result = subprocess.run(py + ' ' + numato_relayread_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay3, shell=True, stdout = subprocess.PIPE)
            relay_status3 = result.stdout.decode().replace('\r\n','')
            print(relay_status3)
            if relay_status3 == "on":
                result = subprocess.run(py + ' ' + numato_relaywrite_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay3 + ' off', shell=True)
                lvalue.append('relay' + Relay3 + ' off dt_time>Startime dt_time>Endtime process end(time over)') #history data
                linemsg_update_flg = linemsg_all
                linemsg_msg = 'relay' + Relay3 + ' off dt_time>Startime dt_time>Endtime process end(time over)'
            elif relay_status3 == "off":
                    result = subprocess.run(py + ' ' + numato_relayread_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay2, shell=True, stdout = subprocess.PIPE)
                    relay_status2 = result.stdout.decode().replace('\r\n','')
                    print(relay_status2)
                    if relay_status2 == "on":
                        result = subprocess.run(py + ' ' + numato_relaywrite_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay2 + ' off', shell=True)
                        lvalue.append('relay' + Relay2 + ' off dt_time>Startime dt_time>Endtime process end(time over)') #history data
                        linemsg_update_flg = linemsg_all
                        linemsg_msg = 'relay' + Relay2 + ' off dt_time>Startime dt_time>Endtime process end(time over)'
                    elif relay_status2 == "off":
                        result = subprocess.run(py + ' ' + numato_relayread_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay1, shell=True, stdout = subprocess.PIPE)
                        relay_status1 = result.stdout.decode().replace('\r\n','')
                        print(relay_status1)
                        if relay_status1 == "on":
                            result = subprocess.run(py + ' ' + numato_relaywrite_py + ' ' + numato_portName + ' ' + numato_baudrate + ' ' + Relay1 + ' off', shell=True)
                            lvalue.append('relay' + Relay1 + ' off dt_time>Startime dt_time>Endtime process end(time over)') #history data
                            linemsg_update_flg = linemsg_all
                            linemsg_msg = 'relay' + Relay1 + ' off dt_time>Startime dt_time>Endtime process end(time over)'
                        elif relay_status1 == "off":
                            lvalue.append('relay all off dt_time>Startime dt_time>Endtime process end(time over)') #history data
                            linemsg_update_flg = linemsg_all
                            linemsg_msg = 'relay all off dt_time>Startime dt_time>Endtime process end(time over)'

    elif dt_now == Endtime:
        lvalue.append('dt_now=Endtime else') #history data
        linemsg_update_flg = linemsg_all
        linemsg_msg = 'dt_now=Endtime else'

#GTI OFF
elif dt_now < Starttime: #before process start
    lvalue.append('dt_time<Starttime dttime<Endtime before process start') #history data
    linemsg_update_flg = linemsg_all
    linemsg_msg = 'dt_time<Starttime dttime<Endtime before process start'
elif dt_now == Starttime:
    lvalue.append('dt_now=Starttime else') #history data
    linemsg_update_flg = linemsg_all
    linemsg_msg = 'dt_now=Starttime else'

print(lvalue)

#write database
retv = cls_epever_control_db.write_control_history(dbPath, lvalue)

if linemsg_update_flg == flgon:
    #request sending LINE message to database
    result = subprocess.run(py + ' ' + linemsg_py + ' r ' + linemsg_dbpath + ' "' + linemsg_msg + '" "' + linemsg_application + '"', shell=True)
           
if retv == lvNormal:
    sys.exit(0)
elif retv == lvError:
    sys.exit(1)
