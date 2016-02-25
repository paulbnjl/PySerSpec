
#-*- coding: UTF-8 -*
############################################################################
############################################################################
#### Person responsible for this pure evil spaghetti code : 			####
#### Paul Bonijol -> paul [.] bnjl ['AT'] gmail [.] com					####
#### Works with python3.4												####
####																	####
#### PySerSpec.py is free software: you can redistribute it and/or		#### 
#### modify it under the terms of the GNU General Public License as     ####
#### published by the Free Software Foundation, either version 3 of the ####
#### License, or (at your option) any later version.					####
#### See http://www.gnu.org/licenses for more information.				####
####																	####
#### I hope this program will be useful to somebody else !				####
#### But please keep in mind that it comes WITHOUT ANY WARRANTY !		#### 
#### If something bad happens, well, sorry ! :(							####
####################### BASELINE CORRECTION CLASS ##########################
############################################################################

class BaseCorr:
	def __init__(self):
		
		self.BASE_CORR_MAX_VAL = 11000 # default max value
		self.BASE_CORR_MIN_VAL = 1900 # default min value
		self.DIFF_VAL_BASECORR = 910 # default measured range (n-m)
		
	def get_BASE_CORR_MAX_VAL(self):
		BASE_CORR_MAX_VAL_control = 0
		while BASE_CORR_MAX_VAL_control == 0:
			BASE_CORR_MAX_VAL_input = input ('Enter the highest wavelength (nm) : \n')
			if BASE_CORR_MAX_VAL_input.isnumeric() == True:
				if 190 <= int(BASE_CORR_MAX_VAL_input) <= 1100:
					self.BASE_CORR_MAX_VAL = int(BASE_CORR_MAX_VAL_input) * 10
					BASE_CORR_MAX_VAL_control = 1
				else:
					print ("ERROR. Value must be in range [190;1100]nm ! Try again. \n")
			else:
				print ("ERROR ! Please enter a numeric value!")
		return self.BASE_CORR_MAX_VAL
			
	def get_BASE_CORR_MIN_VAL(self):
		BASE_CORR_MIN_VAL_control = 0
		while BASE_CORR_MIN_VAL_control == 0:
			BASE_CORR_MIN_VAL_input = input ('Enter the lowest wavelength (nm) : \n')
			if BASE_CORR_MIN_VAL_input.isnumeric() == True:
				if 190 <= int(BASE_CORR_MIN_VAL_input) <= 1100:
					self.BASE_CORR_MIN_VAL = int(BASE_CORR_MIN_VAL_input) * 10
					BASE_CORR_MIN_VAL_control = 1
				else:
					print ("ERROR. Value must be in range [190;1100]nm ! Try again. \n")
			else:
				print ("ERROR ! Please enter a numeric value!")
		return self.BASE_CORR_MIN_VAL

	def test_MAX_MINUS_MIN_BASECORR(self):
		if self.DIFF_VAL_BASECORR >= int(100):
			return 1
		else:
			return 0
			
	def get_DIFF_VAL_BASECORR(self):
		self.DIFF_VAL_BASECORR = (self.BASE_CORR_MAX_VAL/10) - (self.BASE_CORR_MIN_VAL/10)
		return int(self.DIFF_VAL_BASECORR)
