
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

# See the waitinglist as a special listbox (read : listbox with way less functions)
# The metaclass is here completely accessory as I don't even use it for this class but anyway...

class IterableWaitingList(type):
	@classmethod
	def __prepare__(self, name, bases):
		return collections.OrderedDict()
		
	def __new__(meta, name, bases, attrs):
		attrs['_WL_registry'] = [key for key in weakref.WeakSet()
		if key not in ('__module__', '__qualname__')]
		return type.__new__(meta, name, bases, attrs)

	def __call__(cls, *args, **kwargs):
		call_return = type.__call__(cls, *args, **kwargs)
		cls._WL_registry.append(call_return)
		return call_return
        
	def __iter__(self):
		return iter(self._WL_registry)



class Interface_WaitingList(metaclass = IterableWaitingList):
	def __init__(self, parent, name):
		self.list_content = []
		self.parent = parent
		self.name = name
		self.real_send_list = []
		self.object_number_list = []
		self.cassette_label_container = []
	
	def waitinglist(self):
		# The proper waitinglist (tkinter widgets) definition
		waitinglist_subframe=tk.Frame(self.parent)
		waitinglist_suframe_of_the_subframe = tk.Frame(waitinglist_subframe)
		self.waitinglist = tk.Listbox(waitinglist_suframe_of_the_subframe)
		self.waitinglist.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

		yscroll = tk.Scrollbar(waitinglist_suframe_of_the_subframe, command=self.waitinglist.yview,
		 orient=tk.VERTICAL)
		yscroll.pack(side=tk.RIGHT, fill=tk.Y)
		self.waitinglist.configure(yscrollcommand=yscroll.set)
		waitinglist_suframe_of_the_subframe.pack(side=tk.TOP, fill=tk.BOTH)
		
		xscroll = tk.Scrollbar(waitinglist_subframe, command=self.waitinglist.xview, orient=tk.HORIZONTAL)
		xscroll.pack(side=tk.TOP, fill=tk.X)
		self.waitinglist.configure(xscrollcommand=xscroll.set)
		
		waitinglist_subframe.pack(side=tk.TOP, fill=tk.BOTH)
		
		button1 = tk.Button(self.parent, text='Supprimer la ligne', bg='thistle2',
		 command=self.delete_item_from_list)
		button1.pack(side=tk.TOP, fill=tk.BOTH, padx=2, pady=3)
		
		button2 = tk.Button(self.parent, text='Vider la liste', bg='thistle3',
		 command=self.delete_list)
		button2.pack(side=tk.TOP, fill=tk.BOTH, padx=2, pady=3)
		
		for val in self.list_content:
			self.waitinglist.insert(tk.END, val)
			
	def delete_item_from_list(self):
		# Remove the first value from the list
		# And the corresponding entry in the "real" list
		try:
			index = self.waitinglist.curselection()[0]
			self.waitinglist.delete(index)
			del self.real_send_list[index]
			del self.object_number_list[index]
		except IndexError:
			pass
				
	def delete_list(self):
		# Just remove all value, from 0 to the end
		# Also erase the values from the real list
		try:
			self.waitinglist.delete(0,tk.END)
			del self.real_send_list[:]
			del self.object_number_list[:]
		except IndexError:
			pass
  
