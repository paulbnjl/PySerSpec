
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
########################### SIPPER 160 CLASS ###############################
############################################################################


class Sipper160Param:
	
	def __init__(self):
		self.SIPPER160_MODE = ''
		self.SIPPER160_SPEED = ''
		self.SIPPER160_TIME = ''
	
	def get_SIPPER160_PARAMS(self):
				
			SIPPER160_PARAM_CONTROL = 0
			
			while SIPPER160_PARAM_CONTROL == 0:
				print("Sipper 160 parameters : \n")
				sipper160_available_choices_mode = ["1 : Initialize","2 : Aspire","3 : Purge"]
				real_sipper160_available_choices_mode = ['1','2','3']
			
				SIPPER160_MODE_input = ''
				while SIPPER160_MODE_input not in real_sipper160_available_choices_mode:
					for i in range(3):
						print(sipper160_available_choices_mode[i])
					SIPPER160_MODE_input = input('Required action : \n')
					
						
				if SIPPER160_MODE_input == '1':
					self.SIPPER160_MODE = '1'
					self.SIPPER160_SPEED = '1'
					self.SIPPER160_TIME = '1'
					print('Sipper initialized.')
					SIPPER160_PARAM_CONTROL = 1
					return self.SIPPER160_MODE, self.SIPPER160_SPEED, self.SIPPER160_TIME
					
				elif SIPPER160_MODE_input == '2':
					self.SIPPER160_MODE = '2'
					print("Aspiration mode selected.")
					
				elif SIPPER160_MODE_input == '3':
					self.SIPPER160_MODE = '3'
					print("Purge mode selected.")
				
				if self.SIPPER160_MODE in ['2','3']:		
					SIPPER160_SPEED_input = ''
					while SIPPER160_SPEED_input == '':
						print("Speed selection : \n")
						sipper160_available_choices_speed = ["1 : Fast", "2 : Average", "3 : Slow"]
						real_sipper160_available_choices_speed = ['1','2','3']
						
						while SIPPER160_SPEED_input not in real_sipper160_available_choices_speed:
							for i in range(3):
								print(sipper160_available_choices_speed[i])
							SIPPER160_SPEED_input = input('Speed : \n')
							
					self.SIPPER160_SPEED = SIPPER160_SPEED_input
					
					SIPPER160_TIME_input = ''
					while SIPPER160_TIME_input == '':
						print("Duration : \n")
						while SIPPER160_TIME_input not in range(64):
							print ("Type a value between 0 and 64 seconds.")
							SIPPER160_TIME_input = input("Value : ")
					self.SIPPER160_TIME = SIPPER160_TIME_input
					SIPPER160_PARAM_CONTROL = 1
					return self.SIPPER160_MODE, self.SIPPER160_SPEED, self.SIPPER160_TIME
				
				else:
					SIPPER160_PARAM_CONTROL = 1
					return self.SIPPER160_MODE, self.SIPPER160_SPEED, self.SIPPER160_TIME
