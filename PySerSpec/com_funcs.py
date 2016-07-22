
#-*- coding: UTF-8 -*

################################################################################################
###################################### LIBRARIES AND IMPORTS ###################################
################################################################################################

import serial
from intf_widgets import Interface_ComboBox
import time
################################################################################################
################################################################################################
################################################################################################

# This is just a plain PySerial class implementation
# Along with some functions used by buttons that are simply
# The act of sending a defined character line

class PortFunctions():
	def __init__(self):
		self.port = 'COM1'
		self.port_state = ''
		self.writer_status = []
		self.object_number = ''
		
	def port_set(self, port):
		self.port = port
		return self.port
		
	def port_test(self):
		CONNECTEDPORT = ConnectPort()
		self.port_state = ''
		
		while True:
			try:
				CONNECTEDPORT.open_port(self.port)
				CONNECTEDPORT.close_port(self.port)
				#print("Port OK !")
				self.port_state = 1
				break
				
			except serial.SerialException as e2: # wrong port = exception error code 2
				#print("Port not working !")
				#print(self.port)
				self.port_state = 0
				break
				
		return self.port_state		
		
	def button_reset_command(self):
		self.port_test()
		RESET = '\x24\x23\x4b\x52\x0d'
		if self.port_state != 0:
			self.button_reset_command = ConnectPort()
			self.button_reset_command.send_writer(self.port, RESET)
		else:
			pass	
	
	def button_state_command(self):
		self.port_test()
		STATUS_REQUEST = '\x24\x23\x53\x0d'
		if self.port_state != 0:
			self.com_state = ConnectPort()
			self.com_state.send_writer(self.port, STATUS_REQUEST)
			self.com_state.rec_writer_status(self.port)
			self.writer_status
		else:
			pass
	
	def button_eject_command(self):
		self.port_test()
		EJECT_BLADE = '\x24\x23\x4b\x45\x0d'
		if self.port_state != 0:
			self.button_eject_command = ConnectPort()
			self.button_eject_command.send_writer(self.port, EJECT_BLADE)
		else:
			pass

	def button_load_command(self):
		self.port_test()
		LOAD_BLADE = '\x24\x23\x4b\x4c\x0d'
		if self.port_state != 0:
			self.button_load_command = ConnectPort()
			self.button_load_command.send_writer(self.port, LOAD_BLADE)
		else:
			pass
			
	def button_stop_after_cassette_command(self):
		self.port_test()
		STOP_AFTER_CURRENT_LABEL = '\x24\x0d'
		if self.port_state != 0:
			self.button_stop_after_cassette = ConnectPort()
			self.button_stop_after_cassette.send_writer(self.port, STOP_AFTER_CURRENT_LABEL)
		else:
			pass	
		
	def button_stop_after_batch_command(self):
		self.port_test()
		STOP_AFTER_CURRENT_BATCH = '\x24\x23\x43\x0d'
		if self.port_state != 0:
			self.button_stop_after_batch = ConnectPort()
			self.button_stop_after_batch.send_writer(self.port, STOP_AFTER_CURRENT_BATCH)
		else:
			pass
						
	def button_send_command(self, COMMAND):
		self.port_test()
		if self.port_state != 0:
			self.com_send = ConnectPort()
			self.com_send.send_writer(self.port, COMMAND)
		else:
			pass

class ConnectPort():
	def __init__(self):
		# default parameters, as defined by Carousel Microwriter official documentation """
		self.port = serial.Serial()
		self.port.port = ''
		self.port.baudrate = 9600
		self.port.bytesize = serial.EIGHTBITS
		self.port.parity = serial.PARITY_ODD
		self.port.stopbits = serial.STOPBITS_ONE
		self.port.xonxoff = False 
		self.port.rtscts = False 
		self.port.dsrdtr = False
		self.port.timeout = 1
		self.port.write_timeout = 1
		self.port.rts = True
		self.port.dtr = True
		self.port.port = 'COM1' # default
		self.writer_status = []
		self.count = 0
						
	def open_port(self, port):
		self.port.port = port
		self.port.close()
		self.port.open()
		self.port.flushInput()
		self.port.flushOutput()
		#print("Port " + "[" + self.port.port + "]" + " open.")
	
	def close_port(self, port):
		self.port.port = port
		if self.port.isOpen():
			self.port.flushInput()
			self.port.flushOutput()
			self.port.close()
			#print("Port "  + "[" +  self.port.port + "]" + " closed.")
		else:
			pass
			#print("Port "  + "[" +  self.port.port + "]" + " already closed, nothing to do.")
			
	def send_writer(self, port, COMMANDLINE):	 
		try:
			self.open_port(port)
			self.port.write(COMMANDLINE.encode('ascii'))
			#print('Command OK.')
			self.close_port(port)
		except serial.SerialException as e2: # wrong port = exception error code 2
			pass
			#print("Port not working !")
			#print(port)
		
	def rec_writer_status(self, port):
		self.open_port(port)
		line_writer_status=self.port.readline()
		while line_writer_status != b'':
			if line_writer_status != b'':
				self.writer_status.append(line_output)
			else:
				pass
		self.close_port(port)
		return self.writer_status		
