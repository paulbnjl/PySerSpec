
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
########################### WAVELENGTH SET CLASS ###########################
############################################################################

class WaveLengthGet:
	def __init__(self):
		""" Default settings : 500 nm """
		self.WV_VAL = 5500 # default wavelength value for the D2 lamp
		
	def get_WV_VAL(self):
		WV_VAL_control = 0
		while WV_VAL_control == 0:
			WV_VAL_input = input ('Enter wavelength (nm) [default : 550nm] : \n')
			if WV_VAL_input.isnumeric() == True:
				if 190 <= int(WV_VAL_input) <= 1100:
					self.WV_VAL = int(WV_VAL_input)*10
					WV_VAL_control = 1
				else:
					print ("ERROR. Value must be in range [190;1100]nm ! Try again. \n")
			else:
				print ("ERROR ! Please enter a numeric value!")
			return self.WV_VAL
