
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
########################### MEASUREMENT MODE SET CLASS #####################
############################################################################

class MesMode:
	def __init__(self):
		""" Default settings : absorbance=1 """
		self.MODE_VAL = '1'
		
	def get_MODE_VAL(self):			
			available_choices_mes_mode = ["1 : Absorbance (Abs) [default]", "2 : Transmittance (T%)", "3 : Energy", "4 : Exit"]
			mes_mode_real_values = ["1", "2", "3", "4"]
			print("Select measurement mode : \n")
				
			for i in range(4):
				print(available_choices_mes_mode[i])
			mes_mode_choice_val = ''
			while mes_mode_choice_val not in mes_mode_real_values:
				mes_mode_choice_val = input()
			if mes_mode_choice_val in ['1','2','3']:
				self.MODE_VAL = mes_mode_choice_val
				returnchoice = int(mes_mode_choice_val) - int(1)
				print("Measurement mode set to : " + available_choices_mes_mode[int(returnchoice)])
				return self.MODE_VAL
			elif mes_mode_choice_val == '4':
				print("Closing now. Goodbye !")
				end_menu_mode = '1'
				exit()
			else:
				pass
