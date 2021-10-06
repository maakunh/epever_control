#epever_control_watchvc.py
#epever control ver 2.0 Update: 26/08/2021
##Modified: 28/08/2021
#Author: Masafumi Hiura
#URL: https://github.com/maakunh/epever_control
#This code read input/output voltage/current from Epever Charge Controllers. 

import datetime
from decimal import Decimal, getcontext, ROUND_HALF_UP
c = getcontext()
c.rounding = ROUND_HALF_UP
import serial

import epever_control_setting

#setting parameters from epever_controll_setting.py
portNames = epever_control_setting.epever_control_portName()
baudRate = int(epever_control_setting.epever_control_ccbaudrate())
db_unix_socket = epever_control_setting.epever_control_db_unix_socket()
db_user = epever_control_setting.epever_control_db_user()
db_passwd = epever_control_setting.epever_control_db_passwd()
db_host = epever_control_setting.epever_control_db_host()
db_db = epever_control_setting.epever_control_db_db()

import epever_control_common
cls_epever_control_tool = epever_control_common.epever_control_tool()
cls_epever_control_db = epever_control_common.epever_control_db()
cls_epever_contoro_common = epever_control_common.epever_control_commonvalue()
lvNormal = cls_epever_contoro_common.lvNormal
lvError = cls_epever_contoro_common.lvError

# import EPsolarTracerClient
from pyepsolartracer.client import EPsolarTracerClient
# import the server implementation
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

#initialize
Vin = Decimal(0.0).quantize(Decimal('1e-2'))
Cin = Decimal(0.0).quantize(Decimal('1e-2'))
Vout = Decimal(0.0).quantize(Decimal('1e-2'))
Cout = Decimal(0.0).quantize(Decimal('1e-2'))
iCounti = 0
iCounto = 0

try:
	for portName in portNames:
		#check serial connection
		s = serial.Serial(portName)
		s.close()

		#initialize
		lvalue = list()
		# datetime
		dt_now = datetime.datetime.now()
		lvalue.append(dt_now.strftime('%Y/%m/%d %H:%M:%S'))

		# the serial client connection
		serialclient = ModbusClient(method ='rtu', port = portName, baudrate = baudRate, stopbits = 1, bytesize = 8, timeout=1)
		client = EPsolarTracerClient(serialclient = serialclient)
		client.connect()


		# portName
		lvalue.append(portName)

		# response from Charge Controller
		response = cls_epever_control_tool.retry_mesurement2(client, "Charging equipment input voltage")
		print("port: " + portName + " val: " + str(response))
		d = Decimal(response)
		response = d.quantize(Decimal('1e-2'))
		lvalue.append(response)
		if response > 0.0:
			iCounti = iCounti + 1

		Vin = Vin + response

		# "Charging equipment input current"
		response = cls_epever_control_tool.retry_mesurement2(client, "Charging equipment input current")
		print("port: " + portName + " val: " + str(response))
		d = Decimal(response)
		response = d.quantize(Decimal('1e-2'))
		lvalue.append(response)

		Cin = Cin + response

		# "Charging equipment output voltage"
		response = cls_epever_control_tool.retry_mesurement2(client, "Charging equipment output voltage")
		print("port: " + portName + " val: " + str(response))
		d = Decimal(response)
		response = d.quantize(Decimal('1e-2'))
		lvalue.append(response)
		if response > 0.0:
			iCounto = iCounto + 1

		Vout = Vout + response

		# "Charging equipment output current"
		response = cls_epever_control_tool.retry_mesurement2(client, "Charging equipment output current")
		print("port: " + portName + " val: " + str(response))
		d = Decimal(response)
		response = d.quantize(Decimal('1e-2'))
		lvalue.append(response)

		Cout = Cout + response

		print(lvalue)

		ret = cls_epever_control_db.write_record_simple(lvalue)

		client.close() #end serial connection
except Exception:
	# request sending LINE message to database
	linemsg_msg = "ModbusClient Error (" + portName + ") epever_control_watchvc_mysql.py"
	epever_control_common.epever_control_tool().line_message(linemsg_msg)
	epever_control_common.epever_control_tool().server_restart()  # restart server

#Summary
#initialize
lvalue = list()
# datetime
dt_now = datetime.datetime.now()
lvalue.append(dt_now.strftime('%Y/%m/%d %H:%M:%S'))
# portName
lvalue.append('ALL')
#input voltage (average)
if iCounti == 0:
	lvalue.append('0')
else:
	d = Decimal(Vin / iCounti)
	lvalue.append(str(d.quantize(Decimal('1e-2'))))
#input current (sum)
lvalue.append(str(Cin))
#output voltage (average)
if iCounto == 0:
	lvalue.append('0')
else:
	d = Decimal(Vout / iCounto)
	lvalue.append(str(d.quantize(Decimal('1e-2'))))
#output current (sum)
d = Decimal(Cout)
lvalue.append(str(d.quantize(Decimal('1e-2'))))

print(lvalue)

ret = cls_epever_control_db.write_record_simple(lvalue)
