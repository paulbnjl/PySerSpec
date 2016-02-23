
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
########################### DATA TRANSMISSION CLASS ########################
############################################################################


### Libraries ##############################################################
from sig_list import ENQ_SIGNAL, ACK_SIGNAL, EOT_SIGNAL
from spectrum_range import SpectrumScan
from baseline_corr import BaseCorr
from time_scan import TimeScan
from sipper160 import Sipper160Param
from seringe_sipper import SeringeSipperParam
from get_light import LightSource
from get_gain import GainSp
from get_wv import WaveLengthGet
from get_data_acc_time import DataAccSp
from get_mes_mode import MesMode
from connect import ConnectPort
###########################################################################


class SendData(ConnectPort, SpectrumScan, BaseCorr, TimeScan, Sipper160Param, SeringeSipperParam, LightSource, GainSp, WaveLengthGet, DataAccSp, MesMode):
	def __init__(self):
		SpectrumScan.__init__(self)
		BaseCorr.__init__(self)
		TimeScan.__init__(self)
		Sipper160Param.__init__(self)
		SeringeSipperParam.__init__(self)
		LightSource.__init__(self)
		GainSp.__init__(self)
		WaveLengthGet.__init__(self)
		DataAccSp.__init__(self)
		MesMode.__init__(self)
		ConnectPort.__init__(self)
		
	def send_port(self, SIGNAL):
			print("Interrogating machine...")
			self.port.write(ENQ_SIGNAL.encode('ascii'))
			ENQ_request_response = b''
			while ENQ_request_response == b'':
				ENQ_request_response = self.port.read(1)
			if ENQ_request_response == b'\x06':
				print("Machine acknowledged !")
				self.port.write(SIGNAL.encode('ascii'))
				print("Sending request : \n " + SIGNAL)
				
				SIGNAL_request_response = b''
				while SIGNAL_request_response == b'':
					SIGNAL_request_response = self.port.read(1)
				if SIGNAL_request_response == b'\x06\x1b':
					print("Parameter set.")
				elif SIGNAL_request_response == b'\x06':	
					print("Request accepted. Processing...")
					SIGNAL_processed = b''
					while SIGNAL_processed == b'':
						SIGNAL_processed = self.port.read(1)
					print("Request processed ! Waiting EOT signal from the machine to end communication.")
					if SIGNAL_processed == b'\x04':
						self.port.write(ACK_SIGNAL.encode('ascii'))
					else:
						self.port.write(EOT_SIGNAL.encode('ascii'))
						print("ERROR. Machine didn't end communication. Sending EOT.")
				elif SIGNAL_request_response == b'\x06\x04':
					 self.port.write(ACK_SIGNAL.encode('ascii'))
					 print("Request processed ! EOT signal received, ending communication.")
				else:
					print("ERROR. Request refused !")
					print(SIGNAL_request_response)
			else:
				print("ERROR. Machine does not respond.")
