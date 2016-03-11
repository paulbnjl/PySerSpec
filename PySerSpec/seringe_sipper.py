
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
########################### SERINGE SIPPER CLASS ###########################
############################################################################


class SeringeSipperParam:
	
	def __init__(self):
		self.SIPPERSERINGE_MODE = ''
		self.SIPPERSERINGE_SPEED = ''
		self.SIPPERSERINGE_CAPACITY = ''
	
	def get_SERINGESIPPER_PARAMS(self):
				
		SIPPERSERINGE_PARAM_CONTROL = 0
		while SIPPERSERINGE_PARAM_CONTROL == 0:
			print("Seringe sipper parameters : \n")
			seringesipper_available_choices_mode = ["1 : Initialize","2 : Aspiration (valve next to the sample)","3 : Purge (draining valve)","4 : Purge (sample valve)"]
			real_seringesipper_available_choices_mode = ['1','2','3','4']
			
			SIPPERSERINGE_MODE_input = ''
			while SIPPERSERINGE_MODE_input not in real_seringesipper_available_choices_mode:
				for i in range(4):
					print(seringesipper_available_choices_mode[i])
				SIPPERSERINGE_MODE_input = input('Required action : \n')
					
			if SIPPERSERINGE_MODE_input == '1':
				self.SIPPERSERINGE_MODE = '1'
				self.SIPPERSERINGE_SPEED = '1'
				self.SIPPERSERINGE_CAPACITY = '1'
				print('Sipper initialized.')
				SIPPERSERINGE_PARAM_CONTROL = 1
				return self.SIPPERSERINGE_MODE, self.SIPPERSERINGE_SPEED, self.SIPPERSERINGE_CAPACITY
				
			elif SIPPERSERINGE_MODE_input == '2':
				self.SIPPERSERINGE_MODE = SIPPERSERINGE_MODE_input
				print("Aspiration mode selected.")
			elif SIPPERSERINGE_MODE_input == '3':
				self.SIPPERSERINGE_MODE = SIPPERSERINGE_MODE_input
				print("Purge (draining valve) mode selected.")
			elif SIPPERSERINGE_MODE_input == '4':
				self.SIPPERSERINGE_MODE = SIPPERSERINGE_MODE_input
				print("Purge (sample valve) mode selected.")
			else:
				pass
				
			if self.SIPPERSERINGE_MODE in ['2','3','4']:	
				
				SIPPERSERINGE_SPEED_input = ''
				while SIPPERSERINGE_SPEED_input == '':
					print("Speed selection : \n")
					seringesipper_available_choices_speed = ["1 : 1,2 mL/s","2 : 0,6 mL/s","3 : 0,3 mL/s","4 : 0,2 mL/s","5 : 0,1 mL/s"]
					real_seringesipper_available_choices_speed = ['1','2','3', '4','5']
					
					while SIPPERSERINGE_SPEED_input not in real_seringesipper_available_choices_speed:
						for i in range(5):
							print(seringesipper_available_choices_speed[i])
						SIPPERSERINGE_SPEED_input = input('Select speed : \n')
				
				self.SIPPERSERINGE_SPEED = SIPPERSERINGE_SPEED_input
				
				SIPPERSERINGE_CAPACITY_input = ''
				while SIPPERSERINGE_CAPACITY_input == '':
					print("Capacity : \n")
					while SIPPERSERINGE_CAPACITY_input not in range(10):
						print ("Type a value between 0 and 10 mL : ")
						SIPPERSERINGE_CAPACITY_input = input("Value : ")
						
				self.SIPPERSERINGE_CAPACITY = SIPPERSERINGE_CAPACITY_input * 100
				SIPPERSERINGE_PARAM_CONTROL = 1
				return self.SIPPERSERINGE_MODE, self.SIPPERSERINGE_SPEED, self.SIPPERSERINGE_CAPACITY
				
			else:
				SIPPERSERINGE_PARAM_CONTROL = 1
				return self.SIPPERSERINGE_MODE, self.SIPPERSERINGE_SPEED, self.SIPPERSERINGE_CAPACITY
				
