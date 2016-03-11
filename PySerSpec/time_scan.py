
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
########################### TIME SCAN CLASS ################################
############################################################################

class TimeScan:

	def __init__(self):
		""" Default settings : read for one minute """
		self.TIME_VAL = '1'
		self.TIME_UNIT_VAL = '1'
		self.TIME_DATA_POINTS = ''
		self.TIME_RANGE = '2'
		
	def get_TIME_UNIT_VAL(self):			
		choice_unit = ["1 : Seconds", "2 : Minutes"]
		print("Select time unit : \n")
		real_choice_unit = ['1','2']
		for i in range(2):
			print(choice_unit[i])
		TIME_UNIT_VAL_choice = ''
		while TIME_UNIT_VAL_choice not in real_choice_unit:
			TIME_UNIT_VAL_choice = input()
		if TIME_UNIT_VAL_choice == '1':
			self.TIME_UNIT_VAL = 0
		elif TIME_UNIT_VAL_choice == '2':
			self.TIME_UNIT_VAL = 1
		else:
			pass
		return_choice = int(TIME_UNIT_VAL_choice) - int(1)
		print("Time unit set to : " + choice_unit[int(return_choice)])
		return self.TIME_UNIT_VAL
	
	def get_TIME_RANGE(self):
		choice_range = ["1 : [1;10] seconds","2 : [11;100] seconds ","3 : [101;500] seconds","4 : [501;6500] seconds"]
		real_choice_range = ['1', '2', '3', '4']
		print("select time measurement range: \n")
		for i in range(4):
			print(choice_range[i])
		TIME_RANGE_choice = ''
		while TIME_RANGE_choice not in real_choice_range:
			TIME_RANGE_choice = input()
		if TIME_RANGE_choice == '1':
			self.TIME_RANGE = 1
		elif TIME_RANGE_choice == '2':
			self.TIME_RANGE = 2
		elif TIME_RANGE_choice == '3':
			self.TIME_RANGE = 3
		elif TIME_RANGE_choice == '4' :
			self.TIME_RANGE = 4
		else:
			pass			
		return_choice_range = int(TIME_RANGE_choice) - int(1)
		print("Time range : " + choice_range[int(return_choice_range)])
		return self.TIME_RANGE
		
	def get_TIME_VAL(self):
		TIME_VAL_control = 0
		while TIME_VAL_control == 0:
			
			if  self.TIME_UNIT_VAL == 0:
				TIME_VAL_input = input ('Enter time value (seconds) : \n')
				if TIME_VAL_input.isnumeric() == True:
					if 1 <= int(TIME_VAL_input) <= 6500:
						if self.TIME_RANGE == 1:
							if 1 <= int(TIME_VAL_input) <= 10:
								self.TIME_VAL = TIME_VAL_input
								TIME_VAL_control = 1
							else:
								print("Incorrect value, please enter a value within the chosen range !")
								TIME_VAL_control = 0
						elif self.TIME_RANGE == 2:
							if 10 < int(TIME_VAL_input) <= 100:
								self.TIME_VAL = TIME_VAL_input
								TIME_VAL_control = 1
							else:
								print("Incorrect value, please enter a value within the chosen range !")
								TIME_VAL_control = 0	
						elif self.TIME_RANGE == 3:
							if 100 < int(TIME_VAL_input) <= 500:
								self.TIME_VAL = TIME_VAL_input
								TIME_VAL_control = 1
							else:
								print("Incorrect value, please enter a value within the chosen range !")
								TIME_VAL_control = 0	
						elif self.TIME_RANGE == 4:
							if 500 < int(TIME_VAL_input) <= 6500:
								self.TIME_VAL = TIME_VAL_input
								TIME_VAL_control = 1
							else:
								print("Incorrect value, please enter a value within the chosen range !")
								TIME_VAL_control = 0	
						else:
							pass
					else:
						print ("ERROR. Please enter a value greater or equal to 1 and lower or equal to 6500 seconds/108 minutes!")
				else:
					print("ERROR. Please enter a valid number.")
					
			elif self.TIME_UNIT_VAL == 1:
				TIME_VAL_input = input ('Enter time value (minutes) : \n')
				if TIME_VAL_input.isnumeric() == True:
					if 1 <= int(TIME_VAL_input) <= 108:
						self.TIME_VAL = TIME_VAL_input
						TIME_VAL_control = 1
					else:
						print("ERROR. Please enter a value greater or equal to 1 and lower or equal to 6500 seconds/108 minutes!")
				else:
					print("ERROR. Please enter a valid number.")
		return self.TIME_VAL	

	def get_TIME_POINTS(self):
	
		if self.TIME_UNIT_VAL == 0:
			if 1 <= int(self.TIME_VAL) <= 10:
				self.TIME_DATA_POINTS = 10 * int(self.TIME_VAL)
			elif  10 < int(self.TIME_VAL) <= 100:
				self.TIME_DATA_POINTS = self.TIME_VAL
			elif 100 < int(self.TIME_VAL) <= 500:
				self.TIME_DATA_POINTS = 50
			elif int(self.TIME_VAL) > 500:
				self.TIME_DATA_POINTS = 10
						
		elif self.TIME_UNIT_VAL == 1:
			if 1 <= int(self.TIME_VAL) <=108:
				self.TIME_DATA_POINTS = self.TIME_VAL
			elif int(self.TIME_VAL) >= 108:
				self.TIME_DATA_POINTS = 108
		return self.TIME_DATA_POINTS
