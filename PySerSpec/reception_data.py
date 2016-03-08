
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
########################### DATA RECEPTION CLASS ###########################
############################################################################


### Libraries ##############################################################
from sig_list import ENQ_SIGNAL, ACK_SIGNAL, ESC_SIGNAL, EOT_SIGNAL
from ASC_nozzle import AscPosition
from cuvette_position_check import CuvettePosition
from connect import ConnectPort
from data_proc import DataProcessing
############################################################################


class DataReception(ConnectPort, AscPosition, CuvettePosition, DataProcessing):
	def __init__(self):
		ConnectPort.__init__(self)
		CuvettePosition.__init__(self)
		AscPosition.__init__(self)
		DataProcessing.__init__(self)
		self.DATA_output = []
	
	def rec_data(self, SIGNAL):
		self.port.write(ESC_SIGNAL.encode('ascii'))
		
		print("Interrogating machine (ENQ)...")
		self.port.write(ENQ_SIGNAL.encode('ascii'))
		
		ENQ_receive_response = b''
		while ENQ_receive_response == b'':
			ENQ_receive_response = self.port.read(1)
			#print(ENQ_receive_response) #
			
		if ENQ_receive_response == b'\x06':		
			print("Machine acknowledged (ACK) !")
			self.port.write(SIGNAL.encode('ascii'))
			#print("Sending request : \n " + SIGNAL)#
			
			DATA_request_response = b''
			while DATA_request_response == b'':
				DATA_request_response = self.port.read(1)
				#print(DATA_request_response) #
				
				if DATA_request_response in [b'\x06\x05', b'\x06']:
					print("Request accepted (ACK). Processing...")
					
					machine_ENQ = ''
					while machine_ENQ != b'\x05':
						machine_ENQ = self.port.read(1)
						#print(machine_ENQ) #
						
						if machine_ENQ == b'\x1b':
							print("ERROR. Machine sent an ESC signal. Closing now.")
							exit()
							break
							
						else:
							pass
							
					if machine_ENQ == b'\x05':
						self.port.write(ACK_SIGNAL.encode('ascii'))
						
						line_output = ''
						while line_output != b'\x04':
							line_output=self.port.readline()
							self.port.write(ACK_SIGNAL.encode('ascii'))
							
							if line_output != b'\x04':
								self.DATA_output.append(line_output)
							
							else:
								pass
							
						self.port.write(ACK_SIGNAL.encode('ascii'))
						self.port.write(ESC_SIGNAL.encode('ascii'))
						
					else:
						print("ERROR. Message returned : " + machine_ENQ)
						self.port.write(ESC_SIGNAL.encode('ascii'))
						self.port.write(EOT_SIGNAL.encode('ascii'))
						exit()
						break
				
				elif DATA_request_response == b'\x15':
					print("ERROR. Machine refused the command (NAK).")
					self.port.write(ESC_SIGNAL.encode('ascii'))
					self.port.write(EOT_SIGNAL.encode('ascii'))
					exit()
					break
					
				else:
					print("ERROR. No return (ENQ) from the machine.")
					self.port.write(ESC_SIGNAL.encode('ascii'))
					self.port.write(EOT_SIGNAL.encode('ascii'))
					exit()
					break
		else:
			print ("ERROR. Enquiry (ENQ) request refused !")
			self.port.write(ESC_SIGNAL.encode('ascii'))
			self.port.write(EOT_SIGNAL.encode('ascii'))
			exit()
			
		return self.DATA_output
