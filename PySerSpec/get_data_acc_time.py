
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
########################### DATA ACCUMULATION TIME SET CLASS ###############
############################################################################

class DataAccSp:
	def __init__(self):
		
		self.DATA_ACC_VAL = 2
		
	def get_DATA_ACC_VAL(self):			
			available_choices_data_acc = ["1 : 50 ms","2 : 100 ms [default]","3 : 200 ms","4 : Exit"]
			real_choices_data_acc = ["1","2","3","4"]
			print("Select data accumulation time : \n")
			for i in range(4):
				print(available_choices_data_acc[i])
			data_acc_choice_val = ''
			while data_acc_choice_val not in real_choices_data_acc:
				data_acc_choice_val = input()
				
				if data_acc_choice_val in ['1','2','3']:
					self.DATA_ACC_VAL = data_acc_choice_val
					returnchoice = int(data_acc_choice_val) - int(1)
					print("Accumulation time set to " + available_choices_data_acc[int(returnchoice)])
					print("Please note that you will have to correct the baseline again after this.")
					return self.DATA_ACC_VAL
				
				elif data_acc_choice_val == '4':
					print("Closing now. Goodbye !")
					end_menu_dat = '1'
					exit()
				else:
					pass
