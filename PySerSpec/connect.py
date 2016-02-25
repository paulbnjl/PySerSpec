
#-*- coding: UTF-8 -*
############################################################################
############################################################################
#### Person responsible for this pure evil spaghetti code : 			####
#### Paul Bonijol -> paul [.] bnjl ['AT'] gmail [.] com					####
#### Works with python3.4												####
####																	####
#### PySerSpec.py is free software: you can redistribute it and/or      #### 
#### modify it under the terms of the GNU General Public License as     ####
#### published by the Free Software Foundation, either version 3 of the ####
#### License, or (at your option) any later version.					####
#### See http://www.gnu.org/licenses for more information.				####
####																	####
#### I hope this program will be useful to somebody else !				####
#### But please keep in mind that it comes WITHOUT ANY WARRANTY !		#### 
#### If something bad happens, well, sorry ! :(							####
########################### SERIAL CONNECTION CLASS ########################
############################################################################


### Libraries ##############################################################
import serial
############################################################################

### Serial port access #####################################################
class ConnectPort():
	def __init__(self):
		""" default parameters, as defined by Shimadzu UVmin-1240 official documentation """
		self.port = serial.Serial()
		self.port.port = ''
		self.port.baudrate = 9600
		self.port.bytesize = serial.SEVENBITS
		self.port.parity = serial.PARITY_ODD
		self.port.stopbits = serial.STOPBITS_ONE
		self.port.xonxoff = False 
		self.port.rtscts = False 
		self.port.dsrdtr = False
		self.port.timeout = 0.1
		self.port.write_timeout = 0.1
		self.port.rts = True # don't ask me why, it won't work without it
		self.port.dtr = True
		
	def get_port(self):
		available_port = ["1 : COM1", "2 : COM2", "3 : COM3", "4 : COM4", "5 : /dev/ttyS0 (GNU/Linux)", "6 : /dev/ttyUSB0 (GNU/Linux)", "7 : Other port (specify)", '8 : Exit']
		real_available_port_choice = ['1','2','3','4','5','6','7','8']
		print ('Select the serial port connected to the spectrophotometer : \n')
		
		port_choice = ''
		while port_choice not in real_available_port_choice:
			for i in range(8):
				print(available_port[i])
			port_choice = input()
		if port_choice == '1':
			self.port.port = 'COM1'
			print(self.port.port)
			print("Selected interface : COM1")
		elif port_choice == '2':
			self.port.port = 'COM2'
			print("Selected interface : COM2")
		elif port_choice == '3':
			self.port.port = 'COM3'			
			print("Selected interface : COM3")
		elif port_choice == '4':
			self.port.port = 'COM4'
			print("Selected interface : COM4")
		elif port_choice == '5':
			self.port.port = '/dev/ttyS0'
			print("Selected interface : /dev/ttyS0")
		elif port_choice == '6':
			self.port.port =  '/dev/ttyUSB0'
			print("Selected interface : /dev/ttyUSB0")
			
		elif port_choice == '7':
			custom_interface_input = input('Please enter your port name/path and press enter :  \n')
			self.port.port = custom_interface_input
			print("Selected interface : " + custom_interface_input)
			
		elif port_choice == '8':
			print("Closing now. Goodbye !")
			exit()
		else:
			pass
		return self.port.port
				
		
	def open_port(self):
		self.port.close()
		self.port.open()
		self.port.flushInput()
		self.port.flushOutput()
		print("Port open.")
	
	def close_port(self):
		if self.port.isOpen():
			self.port.flushInput()
			self.port.flushOutput()
			self.port.close()
			print("Port closed.")
		else:
			print("Port already closed, nothing to do.")
