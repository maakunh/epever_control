#epever_control_watchvc.py
#epever control ver 2.0 Update: 26/08/2021
##Modified: 28/08/2021
#Author: Masafumi Hiura
#URL: https://github.com/maakunh/epever_control
#This code read input/output voltage/current from Epever Charge Controllers. 

import time
import datetime
import sys
import sqlite3

import epever_control_setting

#setting parameters from epever_controll_setting.py
portNames = epever_control_setting.epever_control_portName()
baudRate = int(epever_control_setting.epever_control_ccbaudrate())
dbPath = epever_control_setting.epever_control_dbpath()

import epever_control_common
cls_epever_control_tool = epever_control_common.epever_control_tool()


# import EPsolarTracerClient
from pyepsolartracer.client import EPsolarTracerClient
from pyepsolartracer.registers import registers,coils
# import the server implementation
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.mei_message import *
from pyepsolartracer.registers import registers,coils
import serial.rs485

#initialize
Vin = 0.0
Cin = 0.0
Vout = 0.0
Cout = 0.0
iCount = 0

# database connection
dbname = dbPath
conn = sqlite3.connect(dbname)
cur = conn.cursor()


for portName in portNames:
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
	# "Charging equipment input voltage"
	response = client.read_input("Charging equipment input voltage")
	strr = str(response)
	print(strr)
	result = cls_epever_control_tool.to_numericval_unit(strr)
	value = cls_epever_control_tool.to_numericval
	lvalue.append(value)
	if value == '-': #response = 'Non'
		value = '0' #extract value
    
	Vin = Vin + float(value)

	# "Charging equipment input current"
	response = client.read_input("Charging equipment input current")
	strr = str(response)
	print(strr)
	result = cls_epever_control_tool.to_numericval_unit(strr)
	value = cls_epever_control_tool.to_numericval
	lvalue.append(value)
	if value == '-': #response = 'Non'
		value = '0' #extract value
		
	Cin = Cin + float(value)

	# "Charging equipment output voltage"
	response = client.read_input("Charging equipment output voltage")
	strr = str(response)
	print(strr)
	result = cls_epever_control_tool.to_numericval_unit(strr)
	value = cls_epever_control_tool.to_numericval
	lvalue.append(value)
	if value == '-': #response = 'Non'
		value = '0' #extract value

	Vout = Vout + float(value)

	# "Charging equipment output current"
	response = client.read_input("Charging equipment output current")
	strr = str(response)
	print(strr)
	result = cls_epever_control_tool.to_numericval_unit(strr)
	value = cls_epever_control_tool.to_numericval
	lvalue.append(value)
	if value == '-': #response = 'Non'
		value = '0' #extract value
		
	Cout = Cout + float(value)

	print(lvalue)

	# record to the database
	try:
		cur.execute("INSERT INTO record_simple VALUES(?, ?, ?, ?, ?, ?)", lvalue)
	except sqlite3.Error as e:
		print(e)

	conn.commit()

	client.close() #end serial connection

	iCount = iCount + 1

#Summary
#initialize
lvalue = list()
# datetime
dt_now = datetime.datetime.now()
lvalue.append(dt_now.strftime('%Y/%m/%d %H:%M:%S'))
# portName
lvalue.append('ALL')
#input voltage (average)
lvalue.append(str(Vin / iCount))
#input current (sum)
lvalue.append(str(Cin))
#output voltage (average)
lvalue.append(str(Vout / iCount))
#output current (sum)
lvalue.append(str(Cout))

print(lvalue)

# record to the database
try:
	cur.execute("INSERT INTO record_simple VALUES(?, ?, ?, ?, ?, ?)", lvalue)
except sqlite3.Error as e:
	print(e)

conn.commit()

conn.close()
