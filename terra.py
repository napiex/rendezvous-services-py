#!/usr/bin/python
import fcntl, struct, time, re


import serial 
import ablib
from ablib import Daisy24
from config_file import DISPLAY_I2C_BUS
from config_file import RS485_PORT, VAISALA_TIMEOUT, VAISALA_BAUDRATE , RS485_PORT	, \
						VAISALA_STOPSBITS, VAISALA_BYTESIZE, VAISALA_PARITY
#from utils  import get_display_device_addrs

NUMS_RE = r"[+-]?((\d+(\.\d*)?)|\.\d+)([eE][+-]?[0-9]+)?"


class Display(object):

	def __init__(self):
		self.addr = self.__get_display_device_addrs()
		self.lcd = Daisy24(DISPLAY_I2C_BUS, self.addr)

	def __get_display_device_addrs(self):
		if ablib.existI2Cdevice(0,0x27):
			return 0x27
		else:
			return 0x3F


	def turn_backlight(self, on=0):
		"""1=on 0=off default to OFF"""
		if on == 0:
			self.lcd.backlightoff()
			return
		self.lcd.backlighton()

	def write_line(self, line_num=1, text="SAY SOMETHING"):
		""" alphanumeric 16X2 chars """
		self.lcd.setcurpos(0,line_num)
		self.lcd.putstring(text)

	def clear(self):
		self.lcd.clear()

class TemperatureSensor(object):

	def __init__(self):
		self.ser_comm = serial.Serial()
		self.ser_comm.port = RS485_PORT
		self.ser_comm.baudrate = VAISALA_BAUDRATE
		self.ser_comm.timeout = VAISALA_TIMEOUT
		self.ser_comm.parity = VAISALA_PARITY
		self.ser_comm.stopbits = VAISALA_STOPSBITS
		self.ser_comm.bytesize = VAISALA_BYTESIZE
		self.ser_comm.open()
		self.fd = self.ser_comm.fileno()
		self.rs485 = struct.pack('hhhhhhhh',1, 0, 0, 0, 0 ,0 ,0 ,0)
		fcntl.ioctl(self.fd,0x542F,self.rs485)
		self.ser_comm.close()

	def read(self, device_oid = 0):
		"""
			Returns a python list(ARRAY) with TEMP, RH, TRH
		"""
		self.ser_comm.open()
		self.ser_comm.flushInput()
		response = self.ser_comm.write('SEND {0}\r'.format(device_oid))
		read = self.ser_comm.read(1000)
		self.ser_comm.close()
		print read
		mesurement = re.findall(NUMS_RE, read)
		print mesurement
		return [m[0] for m in mesurement]


	def set_oid(self, oid = 0):
		self.ser_comm.open()
		address = self.ser_comm.write('ADDR {0}\r'.format(oid))
		self.seer_comm.close()
		return 0
	





