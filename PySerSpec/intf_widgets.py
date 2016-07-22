
#-*- coding: UTF-8 -*

################################################################################################
###################################### LIBRARIES AND IMPORTS ###################################
################################################################################################

import tkinter as tk
import tkinter.ttk as ttk
import os
import weakref
import collections

################################################################################################
################################################################################################
################################################################################################

# This is just a huge bunch of widgets definitions used by the app
# Not much to say about it, all was done accordingly to the tkinter/ttk documentation
# Also there is a lot of junk, unused code here (getters, etc.), but I am too lazy to cleanup !

# About the metaclasses : the idea is that I associate a  "name" to each class and store everything
# As an object (thanks to weakref.weakset) in a ordered dict (hence the collections import).
# It allows to iterate through all declared class that inherit for the metaclasses
# by the mean of the associated classnames

# Also there is a lot of things that should have been elsewhere (type size definition, etc.),
# For the sake of code readability but, yeah, screw it

class IterableComboBox(type):
	@classmethod
	def __prepare__(self, name, bases):
		return collections.OrderedDict()
		
	def __new__(meta, name, bases, attrs):
		attrs['_combobox_registry'] = [key for key in weakref.WeakSet()
		if key not in ('__module__', '__qualname__')]
		
		return type.__new__(meta, name, bases, attrs)

	def __call__(cls, *args, **kwargs):
		call_return = type.__call__(cls, *args, **kwargs)
		cls._combobox_registry.append(call_return)
		return call_return
        
	def __iter__(self):
		return iter(self._combobox_registry)

class Interface_ComboBox(metaclass=IterableComboBox):
	def __init__(self, parent, name):
		self.name = name
		self.parent = parent
		self.value_of_combo = ''
		self.value_of_txt = ''
		self.list_content = []
		self.txt_size_user = ["Grand", "Moyen", "Petit", "Très Petit", '']
		self.txt_size_ascii = '#4'
		self.valuesourcename = ''
		self.value_of_checkbox = 0
		
		self.object_number = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
		
		for i in range (10,51):
			self.object_number.append(i)
		
		self.hopper_number = []
		
		for i in range(1,7):
			self.hopper_number.append(i)
		
		self.port_number = []
		
		for i in range(1,10):
			self.port_number.append('COM' +str(i))
		
		for i in range (0,5):
			self.port_number.append('/dev/ttyS' + str(i))
		
		for i in range (0,5):
			self.port_number.append('/dev/ttyUSB' + str(i))
	
	def combo_rw(self, name, valuesource, default_value, row_label, column_label, row_combo, column_combo):
		self.check_file(valuesource)
		self.open_file(valuesource)
		self.valuesourcename = valuesource
		self.box_value = tk.StringVar()
		self.box = ttk.Combobox(self.parent, textvariable=self.box_value, values=self.list_content, height=50,
		 width=25, exportselection=0, postcommand=self.update_values)
		
		if str(default_value).isnumeric() == True:
			self.box.current(default_value)
		
		else:
			self.box.current(0)
		
		self.box.grid(column=column_combo, row=row_combo)
		self.box.bind("<<ComboboxSelected>>", self.newselection)
		self.box.bind('<Return>', self.update_values_evt)
		self.combo_label(name, column_label, row_label)
	
	def combo_ro(self, name, val, default_value, row_label, column_label, row_combo, column_combo):
		valuesource = []
		
		if val == 'T':
			valuesource = self.txt_size_user
		
		elif val == 'O':
			valuesource = self.object_number
		
		elif val == 'H':
			valuesource = self.hopper_number
		
		elif val == 'P':
			valuesource = self.port_number
		
		else:
			valuesource = val	
		self.box_value = tk.StringVar()
		self.box = ttk.Combobox(self.parent, textvariable=self.box_value, values=valuesource,
		 height=50, width=25, state='readonly', exportselection=0)
		
		if str(default_value).isnumeric() == True:
			self.box.current(default_value)
		
		else:
			self.box.current(0)
		self.box.grid(column=column_combo, row=row_combo)
		
		if val == 'O':
			self.box.bind("<<ComboboxSelected>>", self.newselection)
		
		elif val == 'H':
			self.box.bind("<<ComboboxSelected>>", self.newselection)
		
		elif val == 'P':
			self.box.bind("<<ComboboxSelected>>", self.newselection)	
		
		elif val == 'T':
			self.box.bind("<<ComboboxSelected>>", self.textselection)
		
		else:
			pass		
		
		self.combo_label(name, column_label, row_label)
		
	def combo_object_label(self, name, val, default_value, row_label, column_label, row_combo, column_combo):
		self.valuesource = []
		self.valuesource = val	
		self.box_value = tk.StringVar()
		self.box = ttk.Combobox(self.parent, textvariable=self.box_value, values=self.valuesource,
		 height=50, width=25, state='readonly', exportselection=0, postcommand=self.combo_object_label_update)
		
		if str(default_value).isnumeric() == True:
			self.box.current(default_value)
		
		else:
			self.box.current(0)
		
		self.box.bind("<<ComboboxSelected>>", self.newselection)
		self.box.grid(column=column_combo, row=row_combo)		
		self.combo_label(name, column_label, row_label)
	
	def combo_txt(self, val, default_value, row_label, column_label, row_combo, column_combo):
		valuesource_txt = []
		
		if val == 'T':
			valuesource_txt = self.txt_size_user
		
		else:
			valuesource_txt = val	
		
		self.box_value_txt = tk.StringVar()
		self.box_txt = ttk.Combobox(self.parent, textvariable=self.box_value_txt,
		 values=valuesource_txt, height=50, width=20, state='readonly', exportselection=0)
		
		if str(default_value).isnumeric() == True:
			self.box_txt.current(default_value)
		else:
			self.box_txt.current(0)
		
		self.box_txt.grid(column=column_combo, row=row_combo)
		
		if val == 'T':
			self.box_txt.bind("<<ComboboxSelected>>", self.textselection)
		
		else:
			pass
	
	def get_val(self):
		self.val = ''
		self.val = self.box.get()
		return self.val
	
	def get_txt_size(self):
		self.txt_size = ''
		self.txt_size = self.box_txt.get()
		return self.txt_size
	
	def newselection(self, event):
		self.value_of_combo = self.box.get()
		for classname in [classname for classname in Interface_ComboBoxCST]:
			classname.get_current_index()
		for classname in [classname for classname in Interface_ComboBoxSDL]:
			classname.get_current_index()
			
		for classname in [classname for classname in Interface_ComboBoxCST if classname.value_of_current_selection not in ['',-1]]:
			classname.box.delete(0)
			classname.get_fields()
			classname.box.update_idletasks()
			classname.box.current(classname.value_of_current_selection)
					
		for classname in [classname for classname in Interface_ComboBoxSDL if classname.value_of_current_selection not in ['',-1]]:
			classname.box.delete(0)
			classname.get_fields()
			classname.box.update_idletasks()
			classname.box.current(classname.value_of_current_selection)
			
		return self.value_of_combo
	
	def textselection(self, event):
		self.value_of_txt = self.box_txt.get()
		
		if self.value_of_txt == self.txt_size_user[0]:
			self.txt_size_ascii = '#1'
		
		elif self.value_of_txt == self.txt_size_user[1]:
			self.txt_size_ascii = '#2'
		
		elif self.value_of_txt == self.txt_size_user[2]:
			self.txt_size_ascii = '#3'
		
		elif self.value_of_txt == self.txt_size_user[3]:
			self.txt_size_ascii = '#4'
		
		else:
			self.txt_size_ascii = '#4'
		
		return self.txt_size_ascii	
	
	def combo_label(self, label, column, row):
		self.label = tk.Label(self.parent, text=label)
		self.label.grid(row=row, column=column)
		
	def update_values(self):
		valuesource = self.valuesourcename
		txt = self.open_file(valuesource)
		self.box.configure(values=txt)
		return 'break'

	def combo_object_label_update(self):
		self.box.configure(values=self.valuesource)
		return 'break'

	def update_values_evt(self, evt):
		valuesource = self.valuesourcename
		txt = self.box.get()
		vals = self.box.cget('values')
		
		if not vals:
			self.box.configure(values = (txt, ))
			self.write_file(valuesource)
		
		elif txt not in vals:
			self.box.configure(values = vals + (txt, ))
			self.write_file(valuesource)
		
		return 'break'
		
	def check_file(self, filename):
		owd = os.getcwd()
		
		if os.path.exists('data/lists') == True:
			pass
		
		else:
			os.makedirs('data/lists')
		os.chdir('data/lists')
		
		if os.path.exists(filename + '.txt') == True:
			pass
		
		else:
			list_content = 'none'
			write_file = open(filename + '.txt', "w")
			write_file.write(list_content)
			write_file.close()
		os.chdir(owd)
	
	def open_file(self, filename):	
		owd = os.getcwd()
		
		if os.path.exists('data/lists') == True:
			pass
		
		else:
			os.makedirs('data/lists')
		os.chdir('data/lists')
		read_file = open(filename + '.txt', 'r')
		self.list_content = read_file.readlines()
		read_file.close()
		self.list_content = [val.rstrip() for val in self.list_content]
		os.chdir(owd)
		
		return self.list_content

	def write_file(self, filename):
		owd = os.getcwd()
		self.new_val = self.box.get()
		self.list_content.append(self.new_val)
		
		if os.path.exists('data/lists') == True:
			pass
		
		else:
			os.makedirs('data/lists')
		os.chdir('data/lists')
		write_file = open(filename +'.txt', "w")
		self.list_content_temp = [val + '\n' for val in self.list_content]
		
		for i in range(len(self.list_content_temp)):
			write_file.writelines(self.list_content_temp[i])
		
		write_file.close()
		os.chdir(owd)
		
		
	def checkbox(self, row_checkbox, column_checkbox):
		self.check_value = tk.IntVar()
		self.check = tk.Checkbutton(self.parent, variable=self.check_value,
		 command=self.newselection_checkbox)

		self.check.grid(column=column_checkbox, row=row_checkbox)

	def newselection_checkbox(self):
		self.value_of_checkbox = self.check_value.get()
		return self.value_of_checkbox

################################################################################################	
################################################################################################
################################################################################################

class IterableComboBoxCST(type):
	@classmethod
	def __prepare__(self, name, bases):
		return collections.OrderedDict()
		
	def __new__(meta, name, bases, attrs):
		attrs['_combobox_CST_registry'] = [key for key in weakref.WeakSet()
		if key not in ('__module__', '__qualname__')]
		
		return type.__new__(meta, name, bases, attrs)

	def __call__(cls, *args, **kwargs):
		call_return = type.__call__(cls, *args, **kwargs)
		cls._combobox_CST_registry.append(call_return)
		return call_return
        
	def __iter__(self):
		return iter(self._combobox_CST_registry)

class Interface_ComboBoxCST(metaclass=IterableComboBoxCST):
	def __init__(self, parent, name):
		self.name = name
		self.parent = parent
		self.value_of_combo = ''
		self.value_of_txt = ''
		self.list_content = []
		self.valuesource = []
		self.valuesource_edit = []
		self.valuesourcename = ''
		self.value_of_current_selection = ''
		
	def combo_object_cst(self, name, row_label, column_label, row_combo, column_combo):
		self.box_value = tk.StringVar()
		self.box = ttk.Combobox(self.parent, textvariable=self.box_value,
		 values=self.valuesource, height=50, width=20, state='readonly', exportselection=0,
		  postcommand=self.get_fields)
		self.box.bind("<<ComboboxSelected>>", self.newselection)
		self.box.grid(column=column_combo, row=row_combo)
	
	def combo_object_updated(self):
		self.box_value = tk.StringVar()
		self.box = ttk.Combobox(self.parent, textvariable=self.box_value,
		 values=self.valuesource, height=50, width=20, state='readonly', exportselection=0,
		  postcommand=self.get_fields)
			
	def newselection(self, event):
		self.value_of_combo = self.box.get()
		self.get_current_index()
		return self.value_of_combo
	
	def combo_object_label_update(self):
		self.box.configure(values=self.valuesource)
		return 'break'

	def get_current_index(self):
		self.value_of_current_selection = self.box.current()
		return self.value_of_current_selection
	
	def set_current_index(self):
		self.box.current(self.value_of_current_selection)
		
	def get_fields(self):
		self.valuesource = []
		self.valuesource_edit = []
		for classname in [classname for classname in Interface_ComboBox if classname.name == "object_number"]:
			self.object_number = classname.box.get()
			
		for classname in [classname for classname in Interface_ComboBox
		 if classname.name not in ['port_number_cassette','port_number_slidewriter',
		  'hopper_number', 'object_number']]:
			  
			if classname.value_of_checkbox == 1:
				if classname.box.get() != '':
					chain = ''.join(classname.txt_size_ascii + classname.box.get() + '\x23\x49')
					self.valuesource.append(chain)
					self.valuesource_edit.append(classname.get_val())

				else:
					pass
			
			else:
				if classname.box.get() != '':
					chain = ''.join(classname.txt_size_ascii + classname.box.get())
					self.valuesource.append(chain)
					self.valuesource_edit.append(classname.get_val())
				else:
					pass
		
		for classname in [classname for classname in Interface_EntryBox if classname.name not in ['profile_name']]:
			
			if classname.value_of_checkbox == 1:
				if classname.get_val() != '':
					chain2 = ''.join(classname.txt_size_ascii + classname.get_val() + '\x23\x49')
					self.valuesource.append(chain2)
					self.valuesource_edit.append(classname.get_val())
				else:
					pass
			
			else:
				if classname.get_val() != '':
					chain2 = ''.join(classname.txt_size_ascii + classname.get_val())
					self.valuesource.append(chain2)
					self.valuesource_edit.append(classname.get_val())
				else:
					pass

		self.valuesource.append('\x20\x20\x20\x20')
		self.valuesource_edit.append('....')
		
		self.valuesource.append('\x20\x20')
		self.valuesource_edit.append('..')
		
		self.valuesource.append('')
		self.valuesource_edit.append('')
		
		self.box.configure(values=self.valuesource_edit)
		
		return (self.valuesource, self.valuesource_edit)

################################################################################################
################################################################################################
################################################################################################

class IterableComboBoxSDL(type):
	@classmethod
	def __prepare__(self, name, bases):
		return collections.OrderedDict()
		
	def __new__(meta, name, bases, attrs):
		attrs['_combobox_SDL_registry'] = [key for key in weakref.WeakSet()
		if key not in ('__module__', '__qualname__')]
		
		return type.__new__(meta, name, bases, attrs)

	def __call__(cls, *args, **kwargs):
		call_return = type.__call__(cls, *args, **kwargs)
		cls._combobox_SDL_registry.append(call_return)
		return call_return
        
	def __iter__(self):
		return iter(self._combobox_SDL_registry)

class Interface_ComboBoxSDL(metaclass=IterableComboBoxSDL):
	def __init__(self, parent, name):
		self.name = name
		self.parent = parent
		self.value_of_combo = ''
		self.value_of_txt = ''
		self.list_content = []
		self.valuesource = []
		self.valuesourcename = ''
		self.value_of_current_selection = ''
		
	def combo_object_sdl(self, name, row_label, column_label, row_combo, column_combo):	
		self.box_value = tk.StringVar()
		self.box = ttk.Combobox(self.parent, textvariable=self.box_value,
		 values=self.valuesource, height=50, width=20, state='readonly', exportselection=0,
		  postcommand=self.get_fields)
		self.box.bind("<<ComboboxSelected>>", self.newselection)
		self.box.grid(column=column_combo, row=row_combo)
			
	def newselection(self, event):
		self.value_of_combo = self.box.get()
		self.get_current_index()
		return self.value_of_combo

	def combo_object_label_update(self):
		self.box.configure(values=self.valuesource)
		return 'break'

	def get_current_index(self):
		self.value_of_current_selection = self.box.current()
		return self.value_of_current_selection

	def set_current_index(self):
		self.box.current(self.value_of_current_selection)
		
	def get_fields(self):
		self.valuesource = []
		self.valuesource_edit = []
		for classname in [classname for classname in Interface_ComboBox
		 if classname.name not in ['port_number_cassette','port_number_slidewriter',
		  'hopper_number', 'object_number']]:
			
			if classname.value_of_checkbox == 1:
				if classname.box.get() != '':
					chain = ''.join(classname.txt_size_ascii + classname.box.get() + '\x23\x49')
					self.valuesource.append(chain)
					self.valuesource_edit.append(classname.get_val())
				else:
					pass
			
			else:
				if classname.box.get() != '':
					chain = ''.join(classname.txt_size_ascii + classname.box.get())
					self.valuesource.append(chain)
					self.valuesource_edit.append(classname.get_val())
				else:
					pass
		
		for classname in [classname for classname in Interface_EntryBox if classname.name not in ['profile_name']]:
			
			if classname.value_of_checkbox == 1:
				if classname.get_val() != '':
					chain2 = ''.join(classname.txt_size_ascii + classname.get_val() + '\x23\x49')
					self.valuesource.append(chain2)
					self.valuesource_edit.append(classname.get_val())
				else:
					pass
			
			else:
				if classname.get_val() != '':
					chain2 = ''.join(classname.txt_size_ascii + classname.get_val())
					self.valuesource.append(chain2)
					self.valuesource_edit.append(classname.get_val())
				else:
					pass

		self.valuesource.append('\x20\x20\x20\x20')
		self.valuesource_edit.append('....')
		
		self.valuesource.append('\x20\x20')
		self.valuesource_edit.append('..')
		self.valuesource.append('')
		self.valuesource_edit.append('')
		self.box.configure(values=self.valuesource_edit)
		
		return (self.valuesource, self.valuesource_edit)

################################################################################################
################################################################################################
################################################################################################

class IterableCheckBox(type):
	@classmethod
	def __prepare__(self, name, bases):
		return collections.OrderedDict()
		
	def __new__(meta, name, bases, attrs):
		attrs['_checkbox_registry'] = [key for key in weakref.WeakSet()
		if key not in ('__module__', '__qualname__')]
		
		return type.__new__(meta, name, bases, attrs)

	def __call__(cls, *args, **kwargs):
		call_return = type.__call__(cls, *args, **kwargs)
		cls._checkbox_registry.append(call_return)
		return call_return
        
	def __iter__(self):
		return iter(self._checkbox_registry)

class Interface_CheckBox(metaclass=IterableCheckBox):
	def __init__(self, parent, name):
		self.name = name
		self.parent = parent
		self.value_of_checkbox = 0

	def checkbox(self, row_checkbox, column_checkbox):
		self.check_value = tk.IntVar()
		self.check = tk.Checkbutton(self.parent, variable=self.check_value, command=self.newselection_checkbox)

		self.check.grid(column=column_checkbox, row=row_checkbox)

	def newselection_checkbox(self):
		self.value_of_checkbox = self.check_value.get()
		return self.value_of_checkbox

################################################################################################
################################################################################################
################################################################################################

class IterableListBox(type):

	@classmethod
	def __prepare__(self, name, bases):
		return collections.OrderedDict()
		
	def __new__(meta, name, bases, attrs):
		attrs['_listbox_registry'] = [key for key in weakref.WeakSet()
		if key not in ('__module__', '__qualname__')]
		
		return type.__new__(meta, name, bases, attrs)

	def __call__(cls, *args, **kwargs):
		call_return = type.__call__(cls, *args, **kwargs)
		cls._listbox_registry.append(call_return)
		return call_return
        
	def __iter__(self):
		return iter(self._listbox_registry)
		
class Interface_ListBox(metaclass=IterableListBox):
	def __init__(self, name):
		self.list_content = []
		self.name = name
		self.listbox_name = ''
		self.filename = ''

	def listbox_call(self, listbox_name, filename):
		self.listbox_name = listbox_name
		self.filename = filename
		return self.listbox_name, self.filename
		
	def listbox(self):
		self.name = self
		self.check_file(self.filename)
		self.open_file(self.filename)

		listbox_window = tk.Toplevel()
		listbox_window.wm_title("Entrées : " + self.listbox_name)
		self.listbox = tk.Listbox(listbox_window, width=30, height=10)
		self.listbox.grid(row=0, column=0, sticky=tk.N+tk.S)
		
		yscroll = tk.Scrollbar(listbox_window, command=self.listbox.yview, orient=tk.VERTICAL)
		yscroll.grid(row=0, column=1, sticky=tk.N+tk.S)
		self.listbox.configure(yscrollcommand=yscroll.set)
		
		self.enter1 = tk.Entry(listbox_window, width=30, bg='orange')
		self.enter1.insert(0, 'Choisir ou ajouter entrée')
		self.enter1.grid(row=1, column=0)

		self.enter1.bind('<Return>', self.set_item_list)
		self.enter1.bind('<Double-1>', self.set_item_list)

		button1 = tk.Button(listbox_window, text='Ranger la liste', command=self.sort_list)
		button1.grid(row=2, column=0, sticky=tk.W)
		
		button2 = tk.Button(listbox_window, text='Sauvegarder', command=self.save_listbox_content)
		button2.grid(row=3, column=0, sticky=tk.W)

		button3 = tk.Button(listbox_window, text="Ajouter l'entrée", command=self.add_item_to_list)
		button3.grid(row=2, column=1, sticky=tk.E)

		button4 = tk.Button(listbox_window, text='Supprimer la ligne', command=self.delete_item_from_list)
		button4.grid(row=3, column=1, sticky=tk.E)
		
		button5 = tk.Button(listbox_window, text='Fermer', command=listbox_window.destroy) ###
		button5.grid(row=4, column=0, sticky=tk.W)

		for val in self.list_content:
			self.listbox.insert(tk.END, val)
	 
		self.listbox.bind('<ButtonRelease-1>', self.get_items_from_list)

	def add_item_to_list(self):
	    self.listbox.insert(tk.END, self.enter1.get())
	    
	def delete_item_from_list(self):
		try:
			index = self.listbox.curselection()[0]
			self.listbox.delete(index)
			
		except IndexError:
			pass
        
	def get_items_from_list(self, event):
		index = self.listbox.curselection()[0]
		seltext = self.listbox.get(index)
		self.enter1.delete(0, 50)
		self.enter1.insert(0, seltext)
		
	def set_item_list(self, event):
		try:
			index = self.listbox.curselection()[0]
			self.listbox.delete(index)
			self.save_listbox_content()
			
		except IndexError:
			index = tk.END
			self.listbox.insert(index, self.enter1.get())
			self.save_listbox_content()
	
	def sort_list(self):
		temp_list = list(self.listbox.get(0, tk.END))
		temp_list.sort(key=str.lower)
		self.listbox.delete(0, tk.END)
		
		for item in temp_list:
			self.listbox.insert(tk.END, item)	
	
	def save_listbox_content(self):
		temp_list = list(self.listbox.get(0, tk.END))
		temp_list = [entry + '\n' for entry in temp_list]
		owd = os.getcwd()
		
		if os.path.exists('data/lists') == True:
			pass
		
		else:
			os.makedirs('data/lists')
			
		os.chdir('data/lists')
		save = open(self.filename + ".txt", "w")
		save.writelines(temp_list)
		save.close()
		os.chdir(owd)	
		
	def check_file(self, filename):
		owd = os.getcwd()
		
		if os.path.exists('data/lists') == True:
			pass
		
		else:
			os.makedirs('data/lists')
		os.chdir('data/lists')
		
		if os.path.exists(filename + '.txt') == True:
			pass
		
		else:
			list_content = '?'
			write_file = open(filename + '.txt', "w")
			write_file.write(list_content)
			write_file.close()
		
		os.chdir(owd)
	
	def open_file(self, filename):	
		owd = os.getcwd()
		
		if os.path.exists('data/lists') == True:
			pass
		
		else:
			os.makedirs('data/lists')
		
		os.chdir('data/lists')
		read_file = open(filename + '.txt', 'r')
		self.list_content = read_file.readlines()
		read_file.close()
		self.list_content = [val.rstrip() for val in self.list_content]
		os.chdir(owd)
		
		return self.list_content

	def write_file(self, filename):
		owd = os.getcwd()
		self.new_val = self.box.get()
		self.list_content.append(self.new_val)
		
		if os.path.exists('data/lists') == True:
			pass
		
		else:
			os.makedirs('data/lists')
		
		os.chdir('data/lists')
		write_file = open(filename +'.txt', "w")
		self.list_content_temp = [val + '\n' for val in self.list_content]
		
		for i in range(len(self.list_content_temp)):
			write_file.writelines(self.list_content_temp[i])
		
		write_file.close()
		os.chdir(owd)

################################################################################################
################################################################################################
################################################################################################

class IterableRadioBox(type):
	@classmethod
	def __prepare__(self, name, bases):
		return collections.OrderedDict()
		
	def __new__(meta, name, bases, attrs):
		attrs['_radiobox_registry'] = [key for key in weakref.WeakSet()
		if key not in ('__module__', '__qualname__')]
		
		return type.__new__(meta, name, bases, attrs)

	def __call__(cls, *args, **kwargs):
		call_return = type.__call__(cls, *args, **kwargs)
		cls._radiobox_registry.append(call_return)
		return call_return
        
	def __iter__(self):
		return iter(self._radiobox_registry)

class Interface_RadioBox(metaclass=IterableRadioBox):
	def __init__(self, parent, name):
		self.name = name
		self.parent = parent
		self.value_of_radiobox = 1
		self.radio_control = 0

	def radiobox(self, a,b,c, row_radiobox, column_radiobox):
		self.radio_value = tk.IntVar()
		self.radio_value.set(1)
		self.radio1 = tk.Radiobutton(self.parent, text=a, variable=self.radio_value,
		 value=1, command=self.newselection) # return 0
		self.radio2 = tk.Radiobutton(self.parent, text=b, variable=self.radio_value,
		 value=2, command=self.newselection) # return 1
		self.radio3 = tk.Radiobutton(self.parent, text=c, variable=self.radio_value,
		 value=3, command=self.newselection) # return 2

		self.radio1.grid(column=column_radiobox, row=row_radiobox)
		self.radio2.grid(column=column_radiobox+1, row=row_radiobox)
		self.radio3.grid(column=column_radiobox+2, row=row_radiobox)
		self.radio_control = 1
		
	def newselection(self):
		self.value_of_radiobox = self.radio_value.get()
		return self.value_of_radiobox
	
	def get_radio_val(self):
		if self.radio_control != 0:
			self.value_of_radiobox = self.radio_value.get()
			return self.value_of_radiobox
		else:
			return 1

################################################################################################
################################################################################################
################################################################################################

class IterableEntryBox(type):
	@classmethod
	def __prepare__(self, name, bases):
		return collections.OrderedDict()
		
	def __new__(meta, name, bases, attrs):
		attrs['_entrybox_registry'] = [key for key in weakref.WeakSet()
		if key not in ('__module__', '__qualname__')]
		
		return type.__new__(meta, name, bases, attrs)

	def __call__(cls, *args, **kwargs):
		call_return = type.__call__(cls, *args, **kwargs)
		cls._entrybox_registry.append(call_return)
		return call_return
        
	def __iter__(self):
		return iter(self._entrybox_registry)


class IterableEntryBox(type):
	@classmethod
	def __prepare__(self, name, bases):
		return collections.OrderedDict()
		
	def __new__(meta, name, bases, attrs):
		attrs['_entrybox_registry'] = [key for key in weakref.WeakSet()
		if key not in ('__module__', '__qualname__')]
		
		return type.__new__(meta, name, bases, attrs)

	def __call__(cls, *args, **kwargs):
		call_return = type.__call__(cls, *args, **kwargs)
		cls._entrybox_registry.append(call_return)
		return call_return
        
	def __iter__(self):
		return iter(self._entrybox_registry)

class Interface_EntryBox(metaclass=IterableEntryBox):
	def __init__(self, parent, name):
		self.name = name
		self.parent = parent
		self.value_of_entry = ''
		self.sup_data = []
		self.value_of_checkbox = 0
		self.txt_size_user = ["Grand", "Moyen", "Petit", "Très Petit", '']
		self.txt_size_ascii = '#4'


	def entry_free(self, name, row_label, column_label, row_entry, column_entry):
		self.entry_value = tk.StringVar()
		self.entry = tk.Entry(self.parent, textvariable=self.entry_value,
		 width=28, exportselection=0)

		self.entry.grid(column=column_entry, row=row_entry)
		self.entry.bind('<KeyPress>', self.newselection)
		self.entry.bind('<Button-1>', self.newselection)
		self.entry_label(name, column_label, row_label)

	def entry_label(self, label, column, row):
		self.label = tk.Label(self.parent, text=label)
		self.label.grid(row=row, column=column)

	def newselection(self, event):
		self.value_of_entry = self.entry.get()
		if self.name != 'profile_name':
			for classname in [classname for classname in Interface_ComboBoxCST if classname.value_of_current_selection not in ['', '-1']]:
				classname.get_fields()
				classname.box.update_idletasks()
				classname.box.current(classname.value_of_current_selection)
			
			for classname in [classname for classname in Interface_ComboBoxSDL if classname.value_of_current_selection not in ['', '-1']]:
				classname.get_fields()
				classname.box.update_idletasks()
				classname.box.current(classname.value_of_current_selection)	
		else:
			pass
		
		return self.value_of_entry
	
	def get_val(self):
		val = self.entry.get()
		return val
		
	def get_txt_size(self):
		self.txt_size = ''
		self.txt_size = self.box_txt.get()
		return self.txt_size
		
	def checkbox(self, row_checkbox, column_checkbox):
		self.check_value = tk.IntVar()
		self.check = tk.Checkbutton(self.parent, variable=self.check_value,
		 command=self.newselection_checkbox)

		self.check.grid(column=column_checkbox, row=row_checkbox)

	def newselection_checkbox(self):
		self.value_of_checkbox = self.check_value.get()
		return self.value_of_checkbox
	
	def combo_txt(self, val, default_value, row_label, column_label, row_combo, column_combo):
		valuesource_txt = []
		
		if val == 'T':
			valuesource_txt = self.txt_size_user
		
		else:
			valuesource_txt = val	
		
		self.box_value_txt = tk.StringVar()
		self.box_txt = ttk.Combobox(self.parent, textvariable=self.box_value_txt,
		 values=valuesource_txt, height=50, width=20, state='readonly', exportselection=0)
		
		if str(default_value).isnumeric() == True:
			self.box_txt.current(default_value)
		
		else:
			self.box_txt.current(0)
		
		self.box_txt.grid(column=column_combo, row=row_combo)
		
		if val == 'T':
			self.box_txt.bind("<<ComboboxSelected>>", self.textselection)
		
		else:
			pass
		
	def textselection(self, event):
		self.value_of_txt = self.box_txt.get()
	
		if self.value_of_txt == self.txt_size_user[0]:
			self.txt_size_ascii = '#1'
			
		elif self.value_of_txt == self.txt_size_user[1]:
			self.txt_size_ascii = '#2'
			
		elif self.value_of_txt == self.txt_size_user[2]:
			self.txt_size_ascii = '#3'
			
		elif self.value_of_txt == self.txt_size_user[3]:
			self.txt_size_ascii = '#4'
			
		else:
			self.txt_size_ascii = '#4'
			
		return self.txt_size_ascii

