
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
########################### GAIN SET CLASS #################################
############################################################################

class GainSp:
	def __init__(self):
		""" Default settings : gain=1 """
		self.GAIN_VAL = '3'
			
	def get_GAIN_VAL(self):			
			available_choices_gain = ["1", "2", "3 [default]", "4", "5", "6", "7 : Exit"]
			print("Select gain factor (1 to 6) :  \n")
			for i in range(7):
				print(available_choices_gain[i])
			gain_choice_val = ''
			while gain_choice_val not in available_choices_gain:
				gain_choice_val = input()
				if gain_choice_val in ['1','2','3','4','5','6']:
					self.GAIN_VAL = gain_choice_val
					print("Gain set to : " + available_choices_gain[int(gain_choice_val)-1])
					return self.GAIN_VAL
				else:
					print("Closing now. Goodbye !")
					end_menu_gain = '1'
					exit()
