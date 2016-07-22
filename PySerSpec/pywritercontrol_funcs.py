
#-*- coding: UTF-8 -*

################################################################################################
###################################### LIBRARIES AND IMPORTS ###################################
################################################################################################

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import os
import datetime
import time
import threading
import re

from intf_widgets import (Interface_ComboBoxCST, Interface_ComboBoxSDL,
 Interface_RadioBox, Interface_ComboBox, Interface_EntryBox, Interface_CheckBox)
from com_funcs import PortFunctions, ConnectPort
from itf_wait_list import Interface_WaitingList
from itf_wt_set import Interface_TimeSetWindow

################################################################################################
################################################################################################
################################################################################################

class Special_Functions():
	def __init__(self, parent):
		# Oh god too much unused variables, I have to pylint this seriously!
		self.slide_sleep_time = 15 # slides : ideally 12-25 sec, depending on the label size
		self.cassette_sleep_time = 8 # cassette : around 8-10 sec, depending on the label size
		self.count = ''
		self.parent = parent
		self.cassette_val_list_simple = []
		self.cassette_val_list_real = []
		self.var_time = ''
		self.cassettewriter_port = ''
		self.object_number = ''
		self.hopper_number = ''
		self.slidelabel_val_list_simple = []
		self.slidelabel_val_list_real = []
		self.cassette_control = ''
		self.slide_control = ''
		self.cst_nb = ''
		self.send_nb = ''
		self.slide_nb = ''
		self.queued_cst_nb = ''
		self.queued_slide_nb = ''
		self.cst_line1 = []
		self.cst_line2 = []
		self.cst_line3 = []
		self.sdl_line1 = []
		self.sdl_line2 = []
		self.sdl_line3 = []
		self.sdl_line4 = []
		self.sdl_line5 = []
		self.cst_line1_j = ''
		self.cst_line2_j = ''
		self.cst_line3_j = ''
		self.sdl_line1_j = ''
		self.sdl_line2_j = ''
		self.sdl_line3_j = ''
		self.sdl_line4_j = ''
		self.sdl_line5_j = ''
		self.cassette_line_count = 0
		self.slide_line_count = 0
		self.list_entrybox_content = []
		self.list_combobox_content = []
		self.list_comboboxcst_content = []
		self.list_comboboxsdl_content = []
		self.label = []
		self.label_cst = []
		self.last_inc_char = ''
		self.checked_box_val = 0
		self.break_current_command = ''
		self.cassette_label_container = []
		self.slide_label_container = []
		
	def run_sc_thr(self):
		# Ok, this may be not the best way to handle that, but consider this
		# Tkinter is single threaded. This means that if we launch a function
		# from the main thread, every element of the tkinter interface will be
		# freezed until the end of this function execution.
		# send_command() execution is long, thanks to the time.sleep() everywhere
		# put to be sure that the machine won't skip labels...
		# And the problem is that we want the interface to be still responsive
		# for instance, to send a "stop" command if something goes wrong in the
		# labelling process
		# So we launch send_command() in a separate thread and in the meantime we
		# update the main thread to keep it unfrozen
		
		self.parent.update_idletasks()
		sc_thr = threading.Thread(target=self.send_command)
		sc_thr.start()

	def get_time(self):
		# Simple function to get the day/month/year
		# Initially I planned to retrieve the value in the label organisation fields
		# But it was useless to the technician so... Now it's just for decoration really
		
		self.var_time = datetime.datetime.now().strftime("%d/%m/%Y")
		return self.var_time
			
	def save_profile(self):
		# Allow to save a text file
		# first, test if the data folder exists, and create it otherwise
		# Then use filedialog.asksaveasfilename to obtain from the profile name
		# and save a txt file accordingly
		# if this file exist (security check) and is a txt (filename is changed otherwise)
		# Then it continues by opening this file in writing mode
		# By iterating in fields metaclasses, we store the current field content in lists
		# And write the list content to the profile.txt file.
		
		
		# Create the list we will use to save contents from all the fields
		self.list_entrybox_content = []
		self.list_combobox_content = []
		self.list_comboboxcst_content = []
		self.list_comboboxsdl_content = []
		self.list_comboboxcst_position = []
		self.list_comboboxsdl_position = []
		# Obtain and store the working directory
		owd = os.getcwd()
		
		# Check if a data/ folder exist. We store all txt file there
		# If it doesn't, create this folder
		# (Also, there is a problem somewhere if it's the case)
		if os.path.exists('data/') == True:
			pass
		else:
			os.makedirs('data/')
		
		# Change to the data/ folder	
		os.chdir('data/')
		
		# open a standard tkinter "save file" window
		# filename variable will store the user choice concerning
		# the name of the file (I know, right ?)
		
		filename = filedialog.asksaveasfilename(
		filetypes = [('text files', '.txt')],
		initialfile = 'profil')
		
		# A little condition to prevent some file extension annoyance...
		if '.txt' not in filename:
			filename = str(filename) + '.txt'
		else:
			pass
		
		# Now we write everything in our filename.txt file
		# General idea is that we look for a specific (type of) field(s)
		# store all in the corresponding list
		# the write this list line per line (hence the \n)
		# and after that write a #### line to mark a separation between
		# each (type of) field(s)
		# As the number of fields of this app is fixed, we know the position
		# taken in the txt file for each field value, so it will be way
		# easier to retrieve them with the load() function
			
		# Do things if the user actually put a name for his profile.txt file
		# Do nothing otherwise	
		if filename:
			write_profile = open(filename, "w")
			control = '##########PROFILE##########'
			write_profile.write(control)
			
			for classname in Interface_EntryBox:
				if 'profile_name' in classname.name:
					profile = classname.get_val()
					write_profile.write('\n####################\n')
					write_profile.write(profile)
					write_profile.write('\n####################\n')
				else:
					self.list_entrybox_content.append(classname.get_val())
			
			for i in range(len(self.list_entrybox_content)):
				write_profile.write(self.list_entrybox_content[i] + '\n')
			write_profile.write('####################\n')
			
			for classname in Interface_ComboBox:
				self.list_combobox_content.append(classname.box.get())
			for i in range(len(self.list_combobox_content)):
				write_profile.write(self.list_combobox_content[i] + '\n')		
			write_profile.write('####################\n')
					
			for classname in Interface_ComboBoxCST:
				classname.get_fields()
				self.list_comboboxcst_content.append(classname.box.get())
				if classname.box.get() != '':
					self.list_comboboxcst_position.append(classname.get_current_index())
				else:
					self.list_comboboxcst_position.append('-1')
					
			for i in range(len(self.list_comboboxcst_content)):
				write_profile.write(self.list_comboboxcst_content[i] + '\n')	
			write_profile.write('####################\n')
				
			for classname in Interface_ComboBoxSDL:
				classname.get_fields()
				self.list_comboboxsdl_content.append(classname.box.get())
				if classname.box.get() != '':
					self.list_comboboxsdl_position.append(classname.get_current_index())
				else:
					self.list_comboboxsdl_position.append('-1')
						
			for i in range(len(self.list_comboboxsdl_content)):
				write_profile.write(self.list_comboboxsdl_content[i] + '\n')
			write_profile.write('####################\n')
			for i in range(len(self.list_comboboxcst_position)):
				write_profile.write(str(self.list_comboboxcst_position[i]) + '\n')	
			write_profile.write('####################\n')
			for i in range(len(self.list_comboboxsdl_position)):
				write_profile.write(str(self.list_comboboxsdl_position[i]) + '\n')	
					
			write_profile.write('####################\n')
			write_profile.write('This is a profile definition for PyWriterControl. Do not edit manually !')
			
			
			
			# Once everything is written, we close the file	
			write_profile.close()
		
		else:
			pass
		
		# Finally, we return to the original working directory
		os.chdir(owd)		

	def load_profile(self):
		# Allow to load a text file
		# first, test if the data folder exists, and create it otherwise
		# Then use filedialog.askopenfile to obtain from the user the required file
		# There it test wether the file is OK or not by looking for "PROFILE" in the first line
		# If it's not, it is probably not a profile.
		# OK this is not really solid but it does the trick anyway so...
		# Profiles.txt are fixed : each field, when saved, goes to a defined position
		# To finish, we iterate through all the fields metaclasses to store in them
		# The values stored at the corresponding lines in the profile.txt file
		
		# Get the original working directory, test if the data/ folder
		# exist, and yada yada. Same as before !
		
		owd = os.getcwd()
		if os.path.exists('data/') == True:
			pass
		else:
			os.makedirs('data/')
			
		os.chdir('data/')
		
		# Open a generic tkinter "open file) window
		# read_profile is the name of the selected file
		read_profile = filedialog.askopenfile(mode='r', filetypes =[("Text File", "*.txt")])
		
		# If something was actually selected (i.e read_profile exist),
		# then we can actually do things
		if read_profile:
			
			# I added a first line with "PROFILE" in it. It is a simple
			# test made to be sure that the end user don't screw things
			# deliberately by selecting the wrong type of text file
			firstline = read_profile.readline()
			if 'PROFILE' in firstline:
				
				# Read line per line, append to a list
				lines = [line.rstrip('\n') for line in read_profile]

				# Fields will be feeded with all the corresponding entries
				# In the list
				# Note that if somebody, for some reason, modify the field order
				# And/or add/remove fields... It is needed to adapt all the "count"
				# and tests in the rest of this def()
				
				for classname in Interface_EntryBox:
						if 'profile_name' in classname.name:
							classname.entry.delete(0,tk.END)
							classname.entry.insert(0, lines[1])
							
				count = 3
				while count <= 6:
					for classname in Interface_EntryBox:
						if 'profile_name' in classname.name:
							pass
						else:
							classname.entry.delete(0, tk.END)
							classname.entry.insert(0, lines[count])
							count += 1
				
				count = 8
				while count <= 20:			
					for classname in Interface_ComboBox:
						classname.box.set(lines[count])
						count += 1
				
				#count = 22
				#while count <= 41:
					#for classname in Interface_ComboBoxCST:
					#	classname.box.set(lines[count])
					# count += 1
				
				#count = 43
				#while count <= 67:
					#for classname in Interface_ComboBoxSDL:
						#classname.box.set(lines[count])
						#count += 1
				
				for classname in Interface_ComboBoxCST:
					classname.get_fields()
				for classname in Interface_ComboBoxSDL:
					classname.get_fields()
				classname.box.update_idletasks()		
				
				count = 69
				while count <= 88 :
					for classname in Interface_ComboBoxCST:
						if lines[count] != '-1':
							classname.box.current(lines[count])
						else:
							pass
						count += 1
				
				count = 90
				while count <= 114 :
					for classname in Interface_ComboBoxSDL:
						if lines[count] != '-1':
							classname.box.current(lines[count])
						else:
							pass
						count += 1				
				classname.box.update_idletasks()
										
			else:
				# If the user try to open a wrong text file, show a pop-up
				# saying so, and doing nothing more afterwards
				warning_pop_up = tk.Toplevel()
				warning_message = ("Erreur : le fichier sélectionné n'est pas un profil valide.")
				popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
				popup.pack()
				btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
				btn_OK.pack()
		
			read_profile.close()
		
		else:
			pass
		
		# Return to the original working directory
		os.chdir(owd)


	def get_cassette_organisation(self):
		# list_simple : the list shown in the waiting queue
		# list_real : the list actually used for the label
		self.cassette_control = 0
		self.cassette_val_list_simple = []
		self.cassette_val_list_real = []

		
		for cassette_fields in Interface_ComboBoxCST:
			# for loop to append all the fields to the lists
			cassette_fields.get_fields()
			
			if (cassette_fields.box.get()) != '':
				self.cassette_control = 1	
				for i in [i for i,x in enumerate(cassette_fields.valuesource_edit) 
				if x == cassette_fields.box.get()]:
					self.cassette_val_list_real.append(cassette_fields.valuesource[i])
					self.cassette_val_list_simple.append(cassette_fields.box.get())
			
			# [....] and [..] are the 4 char and 2 char spacers respectively
			# If the field is empty, append 1 space char
			# note : \x20 is "space" in hexa.
			
			elif (cassette_fields.box.get()) == '....':
				self.cassette_val_list_real.append('\x20\x20\x20\x20')
				self.cassette_val_list_simple.append('    ')
			
			elif (cassette_fields.box.get()) == '..':
				self.cassette_val_list_real.append('\x20\x20')
				self.cassette_val_list_simple.append('  ')
				
			else:
				# No need to append the the "simple list"
				# as we don't want to display char space in it
				self.cassette_val_list_real.append(' ')


		for i in [4,9]:
		# Add one LF marker at the end of the first and second line (cassette : 3 lines max)
			self.cassette_val_list_real[i] = (str(self.cassette_val_list_real[i]) + '#N')

		# Insert at the list start the start char ($) and the feeding hopper number (#H + number)
		# #Gxx, the number of element to label, is fixed
		# at first I used the machine incrementation system #I, but it was not convenient
		# (increment normally for 0 to 9 and then start to do weird things)
		# So now I fix the number and generate one command by object,
		# with the 01 modified appropriately, using a loop and regexes
		# '[' and ']' are here to simplify my life with regexes...
		
		self.cassette_val_list_real.insert(0, '[$#H' + self.hopper_number + '#G01')

		self.cst_list_sep = "|"
		self.cst_list = self.cst_list_sep.join(self.cassette_val_list_simple)
		
		self.cassette_label = "".join(self.cassette_val_list_real)
		
		# Add the END (CR) char (hex format, otherwise won't work for some reason)
		self.cassette_label = self.cassette_label + '\x0d]'
		
		# Port, hopper and object number retrieval
		# All it does is iterating in Interface_ComboBox class instanciations
		# and return the proper value if the class name are fitting
		
		for classname in [classname for classname in Interface_ComboBox]:
			if 'port_number_cassette' in classname.name:
				self.cassettewriter_port = classname.box.get()
			elif 'hopper_number' in classname.name:
				self.hopper_number = classname.box.get()
			elif 'object_number' in classname.name:
				self.object_number = classname.box.get()
			else:
				pass
			
		self.cassette_display_string = str("Cassette(s)" + "||" +  self.cassettewriter_port
		  + "||" + "Hopper : " + self.hopper_number + "||" + "Nombre : " 
		+ self.object_number  + "||" + self.cst_list)
		
		return (self.cassette_label, self.cassette_display_string, self.cassette_control, self.cst_nb)
	
	def get_slide_organisation(self):
		# Same concept as the get_cassette_organisation() method
		# See the previous comment to see how it works, if needed
		self.slide_control = 0
		self.slidelabel_val_list_simple = []
		self.slidelabel_val_list_real = []
		
		for slide_fields in Interface_ComboBoxSDL:
			slide_fields.get_fields()
			
			if (slide_fields.box.get()) != '':
				self.slide_control = 1
				for i in [i for i,x in enumerate(slide_fields.valuesource_edit) if x == slide_fields.box.get()]:
					self.slidelabel_val_list_real.append(slide_fields.valuesource[i])
					self.slidelabel_val_list_simple.append(slide_fields.box.get())
					
			elif (slide_fields.box.get()) == '....':
				self.slidelabel_val_list_real.append('\x20\x20\x20\x20')
				self.slidelabel_val_list_simple.append('    ')		
			elif (slide_fields.box.get()) == '..':
				self.slidelabel_val_list_real.append('\x20\x20')
				self.slidelabel_val_list_simple.append('  ')
			else:
				self.slidelabel_val_list_real.append(' ')
				self.label.append(' ')
		
		# 5 lines max for the slides. Theorically it can goes up to 7,
		# But realistically people at NAMSA Lyon never use more than 5 lines
		# So no need to complexify things for the sake of it
		count = 0
		for i in [4,9,14,19]:
			count +=1
			self.slidelabel_val_list_real[i] = (str(self.slidelabel_val_list_real[i]) + '#N')
			self.label[i] = (str(self.label[i]) + '#N')	
				
		self.sdl_list_sep = "|"
		self.sdl_list = self.sdl_list_sep.join(self.slidelabel_val_list_simple)
		
		self.slidelabel_val_list_real.insert(0, '[$#G01')
		self.slidelabel_label = "".join(self.slidelabel_val_list_real)
		self.slidelabel_label = self.slidelabel_label + '\x0d]'
		
		for classname in [classname for classname in Interface_ComboBox]: 
			if 'port_number_slidewriter' in classname.name:
				self.slidewriter_port = classname.box.get()
			elif 'object_number' in classname.name:
				self.object_number = classname.box.get()
			else:
				pass		
		
		# There is not hopper for the slide writer, so no need to retrive
		# the hopper value. But to keep the display consistent, we add "hopper : N/A"
		# in it (N/A : non applicable)
		self.slide_display_string = str("Lame(s)" + "||" +  self.slidewriter_port  
		+ "||" + "Hopper : N/A " + "||" + "Nombre : " 
		+ self.object_number  + "||" + self.sdl_list)
		
		return (self.slidelabel_label, self.slide_display_string, self.slide_control, self.slide_nb)
	
	def get_cassette_line(self):
		# Store line content (line = 5 field) and concatenate everything
		# This will be required to test the number of characters per line
		self.cst_line1 = []
		self.cst_line2 = []
		self.cst_line3 = []
		self.cst_line1_j = ''
		self.cst_line2_j = ''
		self.cst_line3_j = ''

		for classname in [classname for classname in Interface_ComboBoxCST]:
			if (classname.name in ['cassettelabel_field1','cassettelabel_field2','cassettelabel_field3',
			'cassettelabel_field4', 'cassettelabel_field5']):
				self.cst_line1.append(classname.box.get())
				self.cst_line1_j = "".join(self.cst_line1)
			
			elif (classname.name in ['cassettelabel_field6','cassettelabel_field7','cassettelabel_field8',
			'cassettelabel_field9', 'cassettelabel_field10']):
				self.cst_line2.append(classname.box.get())
				self.cst_line2_j = "".join(self.cst_line2)	  
			
			elif (classname.name in ['cassettelabel_field11','cassettelabel_field12',
			'cassettelabel_field13','cassettelabel_field14','cassettelabel_field15']):
				self.cst_line3.append(classname.box.get())
				self.cst_line3_j = "".join(self.cst_line3)
			
			else:
				pass
				  
		return(self.cst_line1_j, self.cst_line2_j, self.cst_line3_j)
	
	def count_cassette_line_number(self):
		# Simple function to count the number of lines
		# It just look if a line is empty. If it's not, the number of line increment by 1
		self.cst_line1_j, self.cst_line2_j, self.cst_line3_j = self.get_cassette_line()
		self.cassette_line_count = 0
		
		for val in [self.cst_line1_j, self.cst_line2_j, self.cst_line3_j]:
			if val != '':
				self.cassette_line_count += 1
			else:
				pass
				
		return self.cassette_line_count
			  
	def get_slide_line(self):
		# Same as get_cassette_line() function, but for slides 
		# (same thing, but for more lines)
		self.sdl_line1 = []
		self.sdl_line2 = []
		self.sdl_line3 = []
		self.sdl_line4 = []
		self.sdl_line5 = []
		self.sdl_line1_j = ''
		self.sdl_line2_j = ''
		self.sdl_line3_j = ''
		self.sdl_line4_j = ''
		self.sdl_line5_j = ''
				
		for classname in [classname for classname in Interface_ComboBoxSDL]:
			if (classname.name in ['slidelabel_field1','slidelabel_field2','slidelabel_field3',
			'slidelabel_field4', 'slidelabel_field5']):
				self.sdl_line1.append(classname.box.get())
				self.sdl_line1_j = "".join(self.sdl_line1)
				
			elif (classname.name in ['slidelabel_field6','slidelabel_field7','slidelabel_field8','slidelabel_field9','slidelabel_field10']):
			  self.sdl_line2.append(classname.box.get())
			  self.sdl_line2_j = "".join(self.sdl_line2)
		
			elif (classname.name in ['slidelabel_field11','slidelabel_field12',
		 'slidelabel_field13','slidelabel_field14','slidelabel_field15']):
			 self.sdl_line3.append(classname.box.get())
			 self.sdl_line3_j = "".join(self.sdl_line3)
			
			elif (classname.name in ['slidelabel_field16','slidelabel_field17',
		 'slidelabel_field18','slidelabel_field19','slidelabel_field20']):
			 self.sdl_line4.append(classname.box.get())
			 self.sdl_line4_j = "".join(self.sdl_line4)
			
			elif (classname.name in ['slidelabel_field21','slidelabel_field22',
		 'slidelabel_field23','slidelabel_field24', 'slidelabel_field25']):
			 self.sdl_line5.append(classname.box.get())
			 self.sdl_line5_j = "".join(self.sdl_line5)

			else:
				pass
			  
		return(self.sdl_line1_j, self.sdl_line2_j, self.sdl_line3_j, self.sdl_line4_j, self.sdl_line5_j)

	def count_slide_line_number(self):
		# Simple function to count the number of lines
		# It just look if a line is empty. If it's not, the number of line increment by 1
		self.sdl_line1_j, self.sdl_line2_j, self.sdl_line3_j, self.sdl_line4_j, self.sdl_line5_j = self.get_slide_line()
		self.slide_line_count = 0
		
		for val in [self.sdl_line1_j, self.sdl_line2_j, self.sdl_line3_j, self.sdl_line4_j, self.sdl_line5_j]:
			if val != '':
				self.slide_line_count += 1
			else:
				pass
				
		return self.slide_line_count

	def get_increment_number(self):
		# Count the number of checked (val=1) checkboxes
		# Afterwards we will used the return value to test if there is more
		# Than one boxed checked (we want only one field to be incremented per batch)
		
		self.checked_box_val = 0
		for classname in [classname for classname in Interface_ComboBox if classname.value_of_checkbox == 1]:
			self.checked_box_val += 1
			
		for classname in [classname for classname in Interface_EntryBox if classname.value_of_checkbox == 1]:	  
			self.checked_box_val +=1
			
		return self.checked_box_val
		
	def test_char_lines(self):
		# This whole function only purpose is to test if the number of characters, per line
		# and the number of lines, are compatible with the defined text size (according to the machines manuals).
		# It's just a boring spaghetti code piece made of comparisons and conditions really...
		# It is probably possible to do way better, but I am too lazy for that !

		cls1 = self.get_cls_radio()
		
		if cls1.get_radio_val() != 2:
			self.cst_line1, self.cst_line2, self.cst_line3 = self.get_cassette_line()
			self.cst_list, self.cassette_label, self.cassette_display_string, self.cst_nb = self.get_cassette_organisation()
			self.cassette_line_number = self.count_cassette_line_number()
			for classname in Interface_ComboBoxCST:
				classname.valuesource, classname.valuesource_edit = classname.get_fields()	
				if '#1' in self.cassette_label:
					if self.cassette_line_number > 2:
						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : police=grande, deux lignes maximum.")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break
									
					else:
						pass	

					for x in [x for x in [self.cst_line1_j, self.cst_line2_j, self.cst_line3_j] if (len(x) >8)]:
						if x == self.cst_line1_j:
							size = str(len(x))
							line = '1, cassette'
						elif x == self.cst_line2_j:
							size = str(len(x))
							line = '2, cassette'
						elif x == self.cst_line3_j:
							size = str(len(x))
							line = '3, cassette'					 


						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : chaine de caractère trop longue ! \n [Ligne " + line + " : "
						+ size + " caractères] \n 8 caractères maximum par ligne (police : grande) !")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break

				elif '#2' in self.cassette_label:
					if self.cassette_line_number > 4:
						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : police=moyenne, quatre lignes maximum.")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break
										
					else:
						pass

					for x in [x for x in [self.cst_line1_j, self.cst_line2_j, self.cst_line3_j] if (len(x) >13)]:
						if x == self.cst_line1_j:
							size = str(len(x))
							line = '1, cassette'
						elif x == self.cst_line2_j:
							size = str(len(x))
							line = '2, cassette'
						elif x == self.cst_line3_j:
							size = str(len(x))
							line = '3, cassette'


						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : chaine de caractère trop longue ! \n [Ligne " + line + " : "
						+ size + " caractères] \n 13 caractères maximum par ligne (police = moyenne) !")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break
					
				else:
					if self.cassette_line_number > 3:
						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : Cassette, trois lignes maximum.")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break
										
					else:
						pass	
					
					for x in [x for x in [self.cst_line1_j, self.cst_line2_j, self.cst_line3_j] if (len(x) >16)]:
						if x == self.cst_line1_j:
							size = str(len(x))
							line = '1, cassette'
						elif x == self.cst_line2_j:
							size = str(len(x))
							line = '2, cassette'
						elif x == self.cst_line3_j:
							size = str(len(x))
							line = '3, cassette'					 

						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : chaine de caractère trop longue ! \n [Ligne " + line + " : "
						+ size + " caractères] \n 16 caractères maximum par ligne !")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break
							
		elif cls1.get_radio_val() != 1:
			self.sdl_line1, self.sdl_line2, self.sdl_line3, self.sdl_line4, self.sdl_line5 = self.get_slide_line()
			self.sdl_list, self.slidelabel_label, self.slide_display_string, self.slide_nb = self.get_slide_organisation()
			self.slide_line_number = self.count_slide_line_number()
			for classname in Interface_ComboBoxSDL:
				classname.valuesource, classname.valuesource_edit = classname.get_fields()
				if '#1' in self.slidelabel_label:
					if self.slide_line_number > 2:
						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : police=grande, deux lignes maximum.")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break

					else:
						pass	

					for x in [x for x in [self.sdl_line1_j, self.sdl_line2_j, self.sdl_line3_j,
					self.sdl_line4_j, self.sdl_line5_j] if (len(x) >8)]:
						if x == self.sdl_line1_j:
							size = str(len(x))
							line = '1, lame'
						elif x == self.sdl_line2_j:
							size = str(len(x))
							line = '2, lame'
						elif x == self.sdl_line3_j:
							size = str(len(x))
							line = '3, lame'					 
						elif x == self.sdl_line4_j:
							size = str(len(x))
							line = '4, lame'
						elif x == self.sdl_line5_j:
							size = str(len(x))
							line = '5, lame'

						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : chaine de caractère trop longue ! \n [Ligne " + line + " : "
						+ size + " caractères] \n 8 caractères maximum par ligne (police : grande) !")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break

				elif '#2' in self.slidelabel_label:
					if self.slide_line_number > 4:
						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : police=moyenne, quatre lignes maximum.")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break
						
					else:
						pass

					for x in [x for x in [self.sdl_line1_j, self.sdl_line2_j, self.sdl_line3_j,
					self.sdl_line4_j, self.sdl_line5_j] if (len(x) >13)]:
						if x == self.sdl_line1_j:
							size = str(len(x))
							line = '1, lame'
						elif x == self.sdl_line2_j:
							size = str(len(x))
							line = '2, lame'
						elif x == self.sdl_line3_j:
							size = str(len(x))
							line = '3, lame'					 
						elif x == self.sdl_line4_j:
							size = str(len(x))
							line = '4, lame'
						elif x == self.sdl_line5_j:
							size = str(len(x))
							line = '5, lame'

						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : chaine de caractère trop longue ! \n [Ligne " + line + " : "
						+ size + " caractères] \n 13 caractères maximum par ligne (police : moyenne) !")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break					

				else:
					for x in [x for x in [self.sdl_line1_j, self.sdl_line2_j, self.sdl_line3_j,
					self.sdl_line4_j, self.sdl_line5_j] if (len(x) >16)]:				
						if x == self.sdl_line1_j:
							size = str(len(x))
							line = '1, lame'
						elif x == self.sdl_line2_j:
							size = str(len(x))
							line = '2, lame'
						elif x == self.sdl_line3_j:
							size = str(len(x))
							line = '3, lame'					 
						elif x == self.sdl_line4_j:
							size = str(len(x))
							line = '4, lame'
						elif x == self.sdl_line5_j:
							size = str(len(x))
							line = '5, lame'
											
						warning_pop_up = tk.Toplevel()
						warning_message = ("Erreur : chaine de caractère trop longue ! \n [Ligne " + line + " : "
						+ size + " caractères] \n 16 caractères maximum par ligne !")
						popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
						popup.pack()
						btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
						btn_OK.pack()
						return 0
						break
		else:
			pass
				
		return 1
		
	def send_to_queue(self):
		# Retrieve all the values from the organisation fields
		
		label_ctrl = self.test_char_lines()
		# Call the test_char_lines function
		# If there is no char at all in the organisation fields
		# then we do nothing
		if label_ctrl == 0:
			pass
			
		else:
		
			cls1 = self.get_cls_radio()
			cls2 = self.get_cls_list()
			cls3 = self.get_cls_hes_trichrome_checkbutton()
			
			if cls1.get_radio_val() == 1:
				for classname in [classname for classname in Interface_ComboBox if 'object_number' in classname.name]:
					cls2.object_number_list.append(classname.box.get())
				self.cassette_label, self.cassette_display_string, self.cassette_control, self.cst_nb = self.get_cassette_organisation()
				self.queued_cst_nb  = self.cst_nb
				if self.cassette_control == 1:
					if cls3.value_of_checkbox == 1:
						cls2.waitinglist.insert(tk.END, self.cassette_display_string)
						cls2.real_send_list.append(self.cassette_label)
						if 'HES' in self.cassette_display_string:
							self.cassette_display_string =  self.cassette_display_string.replace("HES","TM")
							cls2.waitinglist.insert(tk.END, self.cassette_display_string)
							self.cassette_label = self.cassette_label.replace("HES","TM")
							cls2.real_send_list.append(self.cassette_label)
							
							for classname in [classname for classname in Interface_ComboBox if 'object_number' in classname.name]:
								cls2.object_number_list.append(classname.box.get())
								
						elif 'TM' in self.cassette_display_string:
							self.cassette_display_string = self.cassette_display_string.replace("TM","HES")
							cls2.waitinglist.insert(tk.END, self.cassette_display_string)
							self.cassette_label = self.cassette_label.replace("TM","HES")
							cls2.real_send_list.append(self.cassette_label)
							
							for classname in [classname for classname in Interface_ComboBox if 'object_number' in classname.name]:
								cls2.object_number_list.append(classname.box.get()
								)
						else:
							pass
					
					else:
						cls2.waitinglist.insert(tk.END, self.cassette_display_string)
						cls2.real_send_list.append(self.cassette_label)
				else:
					pass 
			
			elif cls1.get_radio_val() == 2:
				for classname in [classname for classname in Interface_ComboBox if 'object_number' in classname.name]:
					cls2.object_number_list.append(classname.box.get())
				self.slidelabel_label, self.slide_display_string, self.slide_control, self.slide_nb = self.get_slide_organisation()
				self.queued_slide_nb = self.slide_nb
				if self.slide_control == 1:
					if cls3.value_of_checkbox == 1:
						cls2.waitinglist.insert(tk.END, self.slide_display_string)
						cls2.real_send_list.append(self.slidelabel_label)
						if 'HES' in self.slide_display_string:
							self.slide_display_string = self.slide_display_string.replace("HES","TM")
							cls2.waitinglist.insert(tk.END, self.slide_display_string)
							self.slidelabel_label = self.slidelabel_label.replace("HES","TM")
							cls2.real_send_list.append(self.slidelabel_label)
							
							for classname in [classname for classname in Interface_ComboBox if 'object_number' in classname.name]:
								cls2.object_number_list.append(classname.box.get())
								
						elif 'TM' in self.slide_display_string:
							self.slide_display_string = self.slide_display_string.replace("TM","HES")
							cls2.waitinglist.insert(tk.END, self.slide_display_string)
							self.slidelabel_label = self.slidelabel_label.replace("TM","HES")
							cls2.real_send_list.append(self.slidelabel_label)
							
							for classname in [classname for classname in Interface_ComboBox if 'object_number' in classname.name]:
								cls2.object_number_list.append(classname.box.get())
								
						else:
							pass				
					else:
						cls2.waitinglist.insert(tk.END, self.slide_display_string)
						cls2.real_send_list.append(self.slidelabel_label)
				else:
					pass
			
			elif cls1.get_radio_val() == 3:	
				self.cassette_label, self.cassette_display_string, self.cassette_control, self.cst_nb = self.get_cassette_organisation()
				self.queued_cst_nb  = self.cst_nb
				if self.cassette_control == 1:
					for classname in [classname for classname in Interface_ComboBox if 'object_number' in classname.name]:
						cls2.object_number_list.append(classname.box.get())
					if cls3.value_of_checkbox == 1:
						cls2.waitinglist.insert(tk.END, self.cassette_display_string)
						cls2.real_send_list.append(self.cassette_label)
						if 'HES' in self.cassette_display_string:
							self.cassette_display_string = self.cassette_display_string.replace("HES","TM")
							cls2.waitinglist.insert(tk.END, self.cassette_display_string)
							self.cassette_label = self.cassette_label.replace("HES","TM")
							cls2.real_send_list.append(self.cassette_label)
							
							for classname in [classname for classname in Interface_ComboBox if 'object_number' in classname.name]:
								cls2.object_number_list.append(classname.box.get())
								
						elif 'TM' in self.cassette_display_string:
							self.cassette_display_string = self.cassette_display_string.replace("TM","HES")
							cls2.waitinglist.insert(tk.END, self.cassette_display_string)
							self.cassette_label = self.cassette_label.replace("TM","HES")
							cls2.real_send_list.append(self.cassette_label)
							
							for classname in [classname for classname in Interface_ComboBox if 'object_number' in classname.name]:
								cls2.object_number_list.append(classname.box.get())
								
						else:
							pass
							
					else:	
						cls2.waitinglist.insert(tk.END, self.cassette_display_string)
						cls2.real_send_list.append(self.cassette_label)
					
				else:
					pass
				
				self.slidelabel_label, self.slide_display_string, self.slide_control, self.slide_nb = self.get_slide_organisation()	
				self.queued_slide_nb = self.slide_nb
				if self.slide_control == 1:
					for classname in [classname for classname in Interface_ComboBox if 'object_number' in classname.name]:
						cls2.object_number_list.append(classname.box.get())
					if cls3.value_of_checkbox == 1:
						cls2.waitinglist.insert(tk.END, self.slide_display_string)
						cls2.real_send_list.append(self.slidelabel_label)
						
						if 'HES' in self.slide_display_string:
							self.slide_display_string = self.slide_display_string.replace("HES","TM")
							cls2.waitinglist.insert(tk.END, self.slide_display_string)
							self.slidelabel_label = self.slidelabel_label.replace("HES","TM")
							cls2.real_send_list.append(self.slidelabel_label)
							
							for classname in [classname for classname in Interface_ComboBox if 'object_number' in classname.name]:
								cls2.object_number_list.append(classname.box.get())
								
						elif 'TM' in self.slide_display_string:
							self.slide_display_string = self.slide_display_string.replace("TM","HES")
							cls2.waitinglist.insert(tk.END, self.slide_display_string)
							self.slidelabel_label = self.slidelabel_label.replace("TM","HES")
							cls2.real_send_list.append(self.slidelabel_label)
							
							for classname in [classname for classname in Interface_ComboBox if 'object_number' in classname.name]:
								cls2.object_number_list.append(classname.box.get())
								
						else:
							pass
							
					else:
						cls2.waitinglist.insert(tk.END, self.slide_display_string)
						cls2.real_send_list.append(self.slidelabel_label)
				else:
					pass
			
			else:
				pass
				
			cls2.waitinglist.update_idletasks()
			
	def send_command(self):
		# Function to send the actual character line to the machines
		# Discriminate wether it's aimed for the cassette writer or the
		# slide writer
		# time.sleep(x) are here to account for the sluggish writing speed
		# of both machines (the thing is that if we don't wait enough
		# commands are skipped, probably because the machines buffers are
		# not that big
			
		if self.get_increment_number() > 1:
			warning_pop_up = tk.Toplevel()
			warning_message = ("Erreur : trop d'incréments, merci de décocher des cases.\n" 
			+ " Un seul champ maximum par série ! \n" 
			+ "[Nombre de cases cochées : " + str(self.get_increment_number()) + "]")
			popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=50)
			popup.pack()
			btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
			btn_OK.pack()
			return 0
			
		else:
			pass
		
		for classname in [classname for classname in Interface_TimeSetWindow]:
			self.slide_sleep_time = int(classname.get_sld())
			self.cassette_sleep_time = int(classname.get_cst())
			
		self.break_current_command = ''
		while self.break_current_command  != 1:
			clswl = self.get_cls_list()
			cls_hes_tm = self.get_cls_hes_trichrome_checkbutton()
			send_command = ConnectPort()
			
			# Just a little placeholder to separate lines sent by the different
			# send_command() call
			# Remove this placeholder if already present
			
			if clswl.waitinglist.get(0) == '###   ###   ###':
				clswl.waitinglist.delete(0)
				self.parent.update_idletasks()
			
			else:
				pass
			
			self.count = ''
			clswl.waitinglist.insert(tk.END, '###   ###   ###')
			
			# Now, we will properly send the lines to the machine
			# for this, we instanciate the ConnectPort function (the one who
			# call Pyserial and actually throw things to the machines)
			# and we process our list entries a little
			
			counter = 0
			while self.count != 0:
				print("###")
				print(counter)
				print("###")
				if clswl.waitinglist.get(0) == '###   ###   ###':
					clswl.waitinglist.delete(0)
					self.break_current_command = 1
					break
				
				else:
					self.count = len(clswl.waitinglist.get(0,tk.END)) - 1			
					search_params = r'(?<=\[).+?(?=\])'
					repl_params = r'[0-9]#I'
					cst_nb_params = r'[0-9][0-9]'
					self.send_nb =  re.search(cst_nb_params, clswl.object_number_list[0])
					self.send_nb = self.send_nb.group()
					self.last_inc_char = re.search(repl_params, clswl.real_send_list[0])
					
					if self.last_inc_char != None :
						self.last_inc_char = self.last_inc_char.group()
						self.last_inc_char = re.sub(r'#I', '', self.last_inc_char)
			
					else:
						self.last_inc_char = 0
							
					if "Cassette(s)" in clswl.waitinglist.get(0):
						clswl.cassette_label_container2 = []
						clswl.cassette_label_container = re.findall(search_params, clswl.real_send_list[0])
						
						for j in range(int(self.last_inc_char), ((int(clswl.object_number_list[0]))+1)):
							cassette_label_val = re.sub(repl_params, str(j), clswl.cassette_label_container[0])
							clswl.cassette_label_container2.append(cassette_label_val)	
																
						for x in range(0, int(self.send_nb)):
							print(x+1)
							print(clswl.cassette_label_container2[x])
							send_command.send_writer(self.cassettewriter_port, clswl.cassette_label_container2[x])
							time.sleep(self.cassette_sleep_time)
					
					elif "Lame(s)" in clswl.waitinglist.get(0):
						clswl.slide_label_container2 = []
						clswl.slide_label_container =  re.findall(search_params, clswl.real_send_list[0])
						
						for jj in range(int(self.last_inc_char), ((int(clswl.object_number_list[0]))+1)):
							slide_label_val = re.sub(repl_params, str(jj), clswl.slide_label_container[0])
							clswl.slide_label_container2.append(slide_label_val)
						
						for y in range(0,int(self.send_nb)):
							print(y+1)
							print(clswl.slide_label_container2[y])
							send_command.send_writer(self.slidewriter_port, clswl.slide_label_container2[y])
							time.sleep(self.slide_sleep_time)
						
						
					else:
						pass
					
					clswl.waitinglist.delete(0)
					clswl.object_number_list = clswl.object_number_list[1:]	
					clswl.real_send_list = clswl.real_send_list[1:]	
					clswl.waitinglist.update_idletasks()
					
					waitinglist_size = len(clswl.waitinglist.get(0,tk.END))
					
					if clswl.waitinglist.get(0) == '###   ###   ###':
						clswl.waitinglist.delete(0)
						print("#########")
						clswl.waitinglist.update_idletasks()
						self.parent.update_idletasks()
						self.count = 0
						self.break_current_command = 1
						break
						
					else:
						pass
					
					self.parent.update_idletasks()
					counter +=1
		
	# Following functions are made always using the same pattern
	# Sending a signal through the PortFunctions classes
	
	def eject_command_slide(self):
		for classname in [classname for classname in Interface_ComboBox 
		if 'port_number_slidewriter' in classname.name]:
			self.slidewriter_port = classname.box.get()
		eject_command = PortFunctions()
		eject_command.port_set(self.slidewriter_port)
		eject_command.button_eject_command()
	
	def eject_command_cassette(self):
		for classname in [classname for classname in Interface_ComboBox 
		if 'port_number_cassette' in classname.name]:
			self.cassettewriter_port = classname.box.get()
		eject_command = PortFunctions()
		eject_command.port_set(self.cassettewriter_port)
		eject_command.button_eject_command()
	
	def load_slide_command(self):
		for classname in [classname for classname in Interface_ComboBox 
		if 'port_number_slidewriter' in classname.name]:
			self.slidewriter_port = classname.box.get()
		load_command = PortFunctions()
		load_command.port_set(self.slidewriter_port)
		load_command.button_load_command()
	
	def reset_cassettewriter_command(self):
		for classname in [classname for classname in Interface_ComboBox 
		if 'port_number_cassette' in classname.name]:
			self.cassettewriter_port = classname.box.get()
		reset_command_cassette = PortFunctions()
		reset_command_cassette.port_set(self.cassettewriter_port)
		reset_command_cassette.button_reset_command()
		
	def reset_slidewriter_command(self):
		for classname in [classname for classname in Interface_ComboBox 
		if 'port_number_slidewriter' in classname.name]:
			self.slidewriter_port = classname.box.get()
		reset_command_slide = PortFunctions()
		reset_command_slide.port_set(self.slidewriter_port)
		reset_command_slide.button_reset_command()
		self.break_current_command = 1
	
	def stop_after_cassette_command(self):
		for classname in [classname for classname in Interface_ComboBox 
		if 'port_number_cassette' in classname.name]:
			self.cassettewriter_port = classname.box.get()
		stop_after_cassette_command = PortFunctions()
		stop_after_cassette_command.port_set(self.cassettewriter_port)
		stop_after_cassette_command.button_stop_after_cassette_command()
		
	def stop_after_slide_command(self):
		for classname in [classname for classname in Interface_ComboBox 
		if 'port_number_slidewriter' in classname.name]:
			self.slidewriter_port = classname.box.get()
		stop_after_cassette_command = PortFunctions()
		stop_after_cassette_command.port_set(self.slidewriter_port)
		stop_after_cassette_command.button_stop_after_cassette_command()
		self.break_current_command = 1
		
	# Some functions made to return some specific class names
	
	def get_cls_radio(self):
		# Just return the classname of the radiobuttons
		for classname in [classname for classname in Interface_RadioBox 
		if 'radiobuttons_blade_slide' in classname.name]:
			self.cls = classname
		return self.cls
	
	def get_cls_list(self):
		# Just return the classname of the waiting list
		for classname in [classname for classname in Interface_WaitingList 
		if 'waitinglist' in classname.name]:
			self.clswl = classname
		return self.clswl
	
	def get_cls_hes_trichrome_checkbutton(self):
		# Just return the class name of the HES/trichrome checkbutton
		for classname in [classname for classname in Interface_CheckBox
		if 'hes_and_trichrome_option' in classname.name]:
			self.cls = classname		
		return self.cls
