
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
########################### CUVETTE POSITION CLASS #########################
############################### UNTESTED ! #################################


class CuvettePosition:	
	def __init__(self): pass
		
	def get_CUVETTE_POS(self, DATA_output):			
		pos_1 = set('q1')
		pos_2 = set('q2')
		pos_3 = set('q3')
		pos_4 = set('q4')
		pos_5 = set('q5')
		pos_6 = set('q6')
		
		for cuvette_state in DATA_output:
			if pos_1 & set(cuvette_state):
				print("Currently on position 1.")
			elif pos_2 & set(cuvette_state):
				print("Currently on position 2.")
			elif pos_3 & set(cuvette_state):
				print("Currently on position 3.")
			elif pos_4 & set(cuvette_state):
				print("Currently on position 4.")
			elif pos_5 & set(cuvette_state):
				print("Currently on position 5.")
			elif pos_6 & set(cuvette_state):
				print("Currently on position 6.")
			else:
				print("ERROR. Look if a multi-cell holder or a CPS-240 unit is connected and/or set before checking position again.")
