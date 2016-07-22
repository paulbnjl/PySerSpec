
#-*- coding: UTF-8 -*

################################################################################################
###################################### LIBRARIES AND IMPORTS ###################################
################################################################################################

import tkinter as tk
import os
import weakref
import collections

################################################################################################
################################################################################################
################################################################################################


class Iterable_TimeSetWindow(type):
	@classmethod
	def __prepare__(self, name, bases):
		return collections.OrderedDict()
		
	def __new__(meta, name, bases, attrs):
		attrs['_TS_registry'] = [key for key in weakref.WeakSet()
		if key not in ('__module__', '__qualname__')]
		return type.__new__(meta, name, bases, attrs)

	def __call__(cls, *args, **kwargs):
		call_return = type.__call__(cls, *args, **kwargs)
		cls._TS_registry.append(call_return)
		return call_return
        
	def __iter__(self):
		return iter(self._TS_registry)



class Interface_TimeSetWindow(metaclass = Iterable_TimeSetWindow):
	def __init__(self, name):
		self.list_content = []
		self.name = name
		self.real_send_list = []
		self.object_number_list = []
		self.cassette_label_container = []
		self.time_cst = 8
		self.time_sld = 15
		
	def timewindow(self):
		self.timewindow_subframe=tk.Toplevel()
		
		self.time_cassette_label = tk.Label(self.timewindow_subframe, text='Temps de gravure par cassette (secondes) : ')
		self.time_cassette_label.grid(row=0, column=0)
		self.time_cassette = tk.StringVar()
		self.time_cassette_entry = tk.Entry(self.timewindow_subframe, textvariable=self.time_cassette, width=10, exportselection=0)
		self.time_cassette_entry.insert(0, str(self.time_cst))
		self.time_cassette_entry.bind('<Return>', self.newselection_cst)
		self.time_cassette_entry.bind('<Button-1>', self.newselection_cst)
		self.time_cassette_entry.grid(row=0, column=1)
		
		self.time_slide_label = tk.Label(self.timewindow_subframe, text='Temps de gravure par lames (secondes) : ')
		self.time_slide_label.grid(row=1, column=0)
		self.time_slide = tk.StringVar()
		self.time_slide_entry = tk.Entry(self.timewindow_subframe, textvariable=self.time_slide, width=10, exportselection=0)
		self.time_slide_entry.insert(0, str(self.time_sld))
		self.time_slide_entry.bind('<Return>', self.newselection_sld)
		self.time_slide_entry.bind('<Button-1>', self.newselection_sld)
		self.time_slide_entry.grid(row=1, column=1)
		
		button_close = tk.Button(self.timewindow_subframe, text='OK', command=self.close_tw_window)
		button_close.grid(row=2, column=1, sticky=tk.W)
	
	def newselection_cst(self, event):
		self.time_cst = self.time_cassette_entry.get()	
		return self.time_cst

	def newselection_sld(self, event):
		self.time_sld = self.time_slide_entry.get()
		return self.time_sld
	
	def get_cst(self):
		return self.time_cst
	def get_sld(self):
		return self.time_sld
		
	def close_tw_window(self):
		self.time_cst = self.time_cassette_entry.get()
		self.time_sld = self.time_slide_entry.get()
		if str(self.time_cst).isnumeric():
			if str(self.time_sld).isnumeric():
				self.timewindow_subframe.destroy()
			else:
				warning_pop_up = tk.Toplevel()
				warning_message = ("Erreur [lames] : valeurs numériques uniquement.")
				popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=40)
				popup.pack()
				btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
				btn_OK.pack()
					
		else:
			warning_pop_up = tk.Toplevel()
			warning_message = ("Erreur [cassette] : valeurs numériques uniquement.")
			popup = tk.Label(warning_pop_up, text=warning_message, height=0, width=40)
			popup.pack()
			btn_OK = tk.Button(warning_pop_up, text="OK", bg="ivory2", command=warning_pop_up.destroy)
			btn_OK.pack()	
