#epever_control_watchall.py
#epever control watchall ver 2.0 Create: 28/08/2021
#Author: Masafumi Hiura
#URL: https://github.com/maakunh/epever_control
#This code get data from EPEVER Charge Controllers and write database(epever.db[table: recordall]) 
#This code needs products below...
#->Epever Charge Controller
## https://www.epsolarpv.com/productlist_1_7.html
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

#import time
import datetime
import sys
import serial

import epever_control_setting
import epever_control_common

#read common value
cls_epever_control_common_value = epever_control_common.epever_control_commonvalue()
lvNormal = cls_epever_control_common_value.lvNormal
lvError = cls_epever_control_common_value.lvError

#setting parameters from epever_controll_setting.py
portNames = epever_control_setting.epever_control_portName()
baudRate = int(epever_control_setting.epever_control_ccbaudrate())

# import EPsolarTracerClient
from pyepsolartracer.client import EPsolarTracerClient
#from pyepsolartracer.registers import registers,coils
# import the server implementation
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
#from pymodbus.mei_message import *
#from pyepsolartracer.registers import registers,coils
#import serial.rs485

# database connection
cls_epever_control_db = epever_control_common.epever_control_db()
ret = cls_epever_control_db.read_colname()
cls_epever_control_common_tool = epever_control_common.epever_control_tool()
if ret == lvNormal:
	lstColname = cls_epever_control_db.lstColname
	try:
		for portName in portNames:
			# check serial connection
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

			#read colname from database(colname)
			for col in lstColname:
				response = client.read_input(col)
				strr = str(response)
				cls_epever_control_tool = epever_control_common.epever_control_tool()
				result = cls_epever_control_tool.to_numericval_unit(strr)
				value = cls_epever_control_tool.to_numericval
				#value = cls_epever_control_common_tool.retry_mesurement2(client, col)
				lvalue.append(value)
			print(lvalue)

			# record to the database
			ret = cls_epever_control_db.write_recordall(lvalue)
			if ret == lvError:
				sys.exit(1)

			client.close() #end serial connection
	except Exception:
		# request sending LINE message to database
		linemsg_msg = "ModbusClient Error (" + portName + ") epever_control_watchall_mysql.py"
		epever_control_common.epever_control_tool().line_message(linemsg_msg)
		epever_control_common.epever_control_tool().server_restart()  # restart server

elif ret == lvError:
	sys.exit(1)


