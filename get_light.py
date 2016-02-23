
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
########################### LIGHT SOURCE SET CLASS #########################
############################################################################

class LightSource:
	def __init__(self):
		""" Default settings : D2 LAMP """
		self.LIGHT_VAL = 2
		
	def get_LIGHT_VAL(self):			
			available_choices_LightSource = ["1 : Tungsten-Iode WI", "2 : Deuterium D2 [default]","3 : Optional lamp", "4 : Exit"]
			LightSource_real_values = ["1","2","3","4"]
			print("Select light source : \n")
			for i in range(4):
				print(available_choices_LightSource[i])
			LightSource_choice_val = ''
			while LightSource_choice_val not in LightSource_real_values:
				LightSource_choice_val = input()
				if LightSource_choice_val in ['1','2', '3']:
					self.LIGHT_VAL = LightSource_choice_val
					print("Light source set to : " + available_choices_LightSource[int(LightSource_choice_val)])
					return self.LIGHT_VAL
				elif LightSource_choice_val == '4':
					print("Closing now. Goodbye !")
					end_menu_light = '1'
					exit()
				else:
					pass
