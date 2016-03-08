
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
########################### SPECTRUM SCAN CLASS ############################
############################################################################


class SpectrumScan():
	def __init__(self):

		self.SP_MAX_VAL = 11000 # default max value
		self.SP_MIN_VAL = 1900 # default min value
		self.SPEED_VAL = 1 # default wavelength scan speed
		self.DIFF_VAL = 910 # default difference
		self.MES_STEP = 1 # measurment step, that depend of both the speed and the wavelength difference
		self.DATA_POINTS = 910 # number of measurments points, equal to DIFF_VAL * MES_STEP and =< 2000
			
	def get_SP_MAX_VAL(self):
		SP_MAX_VAL_CONTROL = 0
		while SP_MAX_VAL_CONTROL == 0:
			SP_MAX_VAL_input = input ('Enter the highest wavelength (nm) : \n')
			if SP_MAX_VAL_input.isnumeric() == True:
				if 190 <= int(SP_MAX_VAL_input) <= 1100:
					self.SP_MAX_VAL = int(SP_MAX_VAL_input)*10
					SP_MAX_VAL_CONTROL = 1
				else:
					print ("ERROR. Value must be in range [190;1100]nm ! Try again. \n")
			else:
				print ("ERROR ! Please enter a numeric value!")
		return self.SP_MAX_VAL

	def get_SP_MIN_VAL(self):
		SP_MIN_VAL_control = 0
		while SP_MIN_VAL_control == 0:
			SP_MIN_VAL_input = input ('Enter lowest wavelength (nm) : \n')
			if SP_MIN_VAL_input.isnumeric() == True:
				if 190 <= int(SP_MIN_VAL_input) <= 1100:
					self.SP_MIN_VAL = int(SP_MIN_VAL_input)*10
					SP_MIN_VAL_control = 1
				else:
					print ("ERROR. Value must be in range [190;1100]nm ! Try again. \n")
			else:
				print ("ERROR ! Please enter a numeric value!")		
		return self.SP_MIN_VAL
		
	def get_SPEED_VAL(self):
		if int(self.DIFF_VAL) <= int(100):
			choice1=["1 : 0.1nm", "2 : 0.2nm", "3 : 0.5nm","4 : 1.0nm", "5 : 2.0nm" ]
			available_choices1 = ["1", "2", "3", "4", "5"]
			print("Select the measuring step : \n")
			for i in range(5):
				print(choice1[i])
			choice_val1 = ''
			while choice_val1 not in available_choices1: # Note : this is really, really badly documented ! Correct value table is p63 of the french doc, not in the "computer control" part...
				choice_val1 = input()
			if choice_val1 == '1':
				print("Measuring step : 0.1 nm") # will in fact return values with a 0,2nm step, as it seems the doc is generic and this machine can't reach 0,1nm...
				self.SPEED_VAL = '5'
				self.MES_STEP = '10'
				
			elif choice_val1 == '2':
				print("Measuring step : 0.2 nm")
				self.SPEED_VAL = '4'
				self.MES_STEP = '5'
				
			elif choice_val1 == '3':
				print("Measuring step : 0.5 nm")
				self.SPEED_VAL = '3'
				self.MES_STEP = '2'
				
			elif choice_val1 == '4':
				print("Measuring step : 1.0 nm")
				self.SPEED_VAL = '2'
				self.MES_STEP = '1'
				
			elif choice_val1 == '5':
				print("Measuring step : 2.0 nm")
				self.SPEED_VAL = '1'
				self.MES_STEP = '20'
								
		elif int(100) < int(self.DIFF_VAL) <= int(200):
			choice2=["1 : 0.2nm", "2 : 0.5nm","3 : 1.0nm","4 : 2.0nm"]
			available_choices2 = ["1","2","3","4"]
			print("Select the measuring step : \n")
			for i in range(4):
				print(choice2[i])
			choice_val2 = ''
			while choice_val2 not in available_choices2:
				choice_val2 = input()
			if choice_val2 == '1':
				print("Measuring step : 0.2 nm")
				self.SPEED_VAL = '4'
				self.MES_STEP = '5'
				
			elif choice_val2 == '2':
				print("Measuring step : 0.5 nm")
				self.SPEED_VAL = '3'
				self.MES_STEP = '2'
				
			elif choice_val2 == '3':
				print("Measuring step : 1.0 nm")
				self.SPEED_VAL = '2'
				self.MES_STEP = '1'
				
			elif choice_val2 == '4':
				print("Measuring step : 2.0 nm")
				self.SPEED_VAL = '1'
				self.MES_STEP = '20'
						
		elif  int(200) < int(self.DIFF_VAL) <= int(500):
			choice3=["1 : 0.5nm", "2 : 1.0nm","3 : 2.0nm"]
			available_choices3 = ["1","2","3"]
			print("Select the measuring step : \n")
			for i in range(3):
				print(choice3[i])
			choice_val3 = ''
			while choice_val3 not in available_choices3:
				choice_val3 = input()
			if choice_val3 == '1':
				print("Measuring step : 0.5 nm")
				self.SPEED_VAL = '3'
				self.MES_STEP = '2'
				
			elif choice_val3 == '2':
				print("Measuring step : 1.0 nm")
				self.SPEED_VAL = '2'
				self.MES_STEP = '1'
				
			elif choice_val3 == '3':
				print("Measuring step : 2.0 nm")
				self.SPEED_VAL = '1'
				self.MES_STEP = '20'
			
		elif int(self.DIFF_VAL) > int(500):
			choice4=["1 : 1.0nm", "2 : 2.0nm"]
			available_choices4 = ["1","2"]
			print("Select the measuring step : \n")
			for i in range(2):
				print(choice4[i])
			choice_val4 = ''
			while choice_val4 not in available_choices4:
				choice_val4 = input()
			if choice_val4 == '1':
				print("Measuring step : 1.0 nm")
				self.SPEED_VAL = '2'
				self.MES_STEP = '1'
				
			elif choice_val4 == '2':
				print("Measuring step : 2.0 nm")
				self.SPEED_VAL = '1'
				self.MES_STEP = '20'
			
		return int(self.SPEED_VAL), int(self.MES_STEP)
	
	def get_DIFF_VAL(self):
		self.DIFF_VAL = (self.SP_MAX_VAL / 10) - (self.SP_MIN_VAL / 10)
		return int(self.DIFF_VAL)
	
	def get_DATA_POINTS(self):
		if self.MES_STEP != '20':
			number_of_points = int(self.DIFF_VAL) * int(self.MES_STEP)
		else:
			number_of_points = int(self.DIFF_VAL/2)	
			
		if 1 <= number_of_points <= 2000:
			self.DATA_POINTS = number_of_points
		elif number_of_points >= 2000:
			self.DATA_POINTS = 2000
		elif number_of_points <= 1:
			self.DATA_POINTS = 1	
			
		return self.DATA_POINTS	
		
	def test_MAX_MINUS_MIN(self):
		diff_ok = ''
		if self.DIFF_VAL >= int(100):
			diff_ok = '1'
			
		else:
			diff_ok = '0'
		return diff_ok
