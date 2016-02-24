
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
########################### ASC NOZZLE STATE CLASS #########################
############################### UNTESTED ! #################################

class AscPosition:
	def __init__(self): pass
	def get_ASC_POS(self, DATA_output):	
		asc_down = set('r1')
		asc_up = set('r2')
		
		for asc_state in DATA_output:
			if asc_down & set(asc_state):
				print("ASC nozzle lowered.")
			elif asc_up & set(asc_state):
				print('ASC nozzle raised.')
			else:
				print("ERROR. Look if the ASC nozzle is connected and check the position again.")
