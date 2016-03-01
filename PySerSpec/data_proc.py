
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
########################### DATA PROCESSING CLASS ##########################
############################################################################


import matplotlib.pyplot as plot
import csv
import os
import datetime
# import math
# from decimal import Decimal

class DataProcessing:
	def __init__(self):
		self.PROCESS_DATA = []
		self.ABS_raw = []
		self.ABS_corr = []
		self.TIME = []
		self.WV = []
		
	def data_spectrum(self, DATA_output):
		for val in DATA_output:
			self.PROCESS_DATA.append(val.decode('utf-8'))
		count = 0
		for val in self.PROCESS_DATA:
			self.PROCESS_DATA[count] = val.replace("\x00",'')
			count += 1
		count=0
		for val in self.PROCESS_DATA:
			self.PROCESS_DATA[count] = val.replace("b'",'')
			count += 1
		count=0
		for val in self.PROCESS_DATA:
			self.PROCESS_DATA[count] = val.replace("\x05",'')
			count += 1
		count=0
		for val in self.PROCESS_DATA:
			self.PROCESS_DATA[count] = val.replace("\x04",'')
			count += 1
		count=0
		for val in self.PROCESS_DATA:
			self.PROCESS_DATA[count] = val.replace("\x1b",'')
			count += 1
		count=0
		for val in self.PROCESS_DATA:
			self.PROCESS_DATA[count] = val.replace("'",'')
			count += 1
		count=0
		for val in self.PROCESS_DATA:
			self.PROCESS_DATA[count] = val.replace("\x2c",'')
			count += 1
		count=0
		for val in self.PROCESS_DATA:
			self.PROCESS_DATA[count] = val.replace("\x06",'')
			count += 1
			
		WV_nested = [s.split(' ', 1)[:1] for s in self.PROCESS_DATA]
		self.WV = [val for sublist in WV_nested for val in sublist if val != ""]
		ABS_nested = [s.split(' ', 1)[1:] for s in self.PROCESS_DATA]
		self.ABS_raw = [val for sublist in ABS_nested for val in sublist if val != ""]
		self.ABS_corr = [val for val in self.ABS_raw]
		for i in range(len(self.ABS_corr)):
			if '-' in self.ABS_corr[i]:
				self.ABS_corr[i] = '0'
			else:
				pass
		return self.ABS_corr, self.ABS_raw, self.WV

	def data_time(self, DATA_output):
			for val in DATA_output:
				self.PROCESS_DATA.append(val.decode('utf-8'))
			count = 0
			for val in self.PROCESS_DATA:
				self.PROCESS_DATA[count] = val.replace("\x00",'')
				count += 1
			count=0
			for val in self.PROCESS_DATA:
				self.PROCESS_DATA[count] = val.replace("b'",'')
				count += 1
			count=0
			for val in self.PROCESS_DATA:
				self.PROCESS_DATA[count] = val.replace("\x05",'')
				count += 1
			count=0
			for val in self.PROCESS_DATA:
				self.PROCESS_DATA[count] = val.replace("\x04",'')
				count += 1
			count=0
			for val in self.PROCESS_DATA:
				self.PROCESS_DATA[count] = val.replace("\x1b",'')
				count += 1
			count=0
			for val in self.PROCESS_DATA:
				self.PROCESS_DATA[count] = val.replace("'",'')
				count += 1
			count=0
			for val in self.PROCESS_DATA:
				self.PROCESS_DATA[count] = val.replace("\x2c",'')
				count += 1
			count=0
			for val in self.PROCESS_DATA:
				self.PROCESS_DATA[count] = val.replace("\x06",'')
				count += 1

			TIME_nested = [s.split('  ', 2)[:2] for s in self.PROCESS_DATA]
			self.TIME = [val for sublist in TIME_nested for val in sublist if val != ""]
			self.TIME = [int(float(x))*10 for x in self.TIME]
			ABS_nested = [s.split('  ', 2)[2:] for s in self.PROCESS_DATA]
			self.ABS_raw = [val for sublist in ABS_nested for val in sublist if val != ""]
			self.ABS_corr = [val for val in self.ABS_raw]
			for i in range(len(self.ABS_corr)):
				if '-' in self.ABS_corr[i]:
					self.ABS_corr[i] = '0'
				else:
					pass
			return self.ABS_raw, self.ABS_corr, self.TIME

	def data_value(self, DATA_output):
		for val in DATA_output:
			self.PROCESS_DATA.append(val.decode('utf-8'))
		count = 0
		for val in self.PROCESS_DATA:
			self.PROCESS_DATA[count] = val.replace("\x00",'')
			count += 1
		count=0
		for val in self.PROCESS_DATA:
			self.PROCESS_DATA[count] = val.replace("b'",'')
			count += 1
		count=0
		for val in self.PROCESS_DATA:
			self.PROCESS_DATA[count] = val.replace("\x05",'')
			count += 1
		count=0
		for val in self.PROCESS_DATA:
			self.PROCESS_DATA[count] = val.replace("\x04",'')
			count += 1
		count=0
		for val in self.PROCESS_DATA:
			self.PROCESS_DATA[count] = val.replace("\x1b",'')
			count += 1
		count=0
		for val in self.PROCESS_DATA:
			self.PROCESS_DATA[count] = val.replace("'",'')
			count += 1
		count=0
		for val in self.PROCESS_DATA:
			self.PROCESS_DATA[count] = val.replace("\x2c",'')
			count += 1
		count=0
		for val in self.PROCESS_DATA:
			self.PROCESS_DATA[count] = val.replace("\x06",'')
			count += 1
		count=0	
		for val in self.PROCESS_DATA:
			self.PROCESS_DATA[count] = val.replace("d",'')
			count += 1		
		self.ABS_raw = self.PROCESS_DATA[0]
		self.ABS_corr = self.ABS_raw
		for val in range(len(self.ABS_corr)):
			if '-' in self.ABS_corr:
				self.ABS_corr = '0'
			else:
				pass
				
		return self.ABS_corr, self.ABS_raw	
		
	def data_plot(self, title_x_axis, title_y_axis,val_ax, val_or):
		for i in range(len(val_ax)):
			if val_ax[i] == '':
				val_ax[i] = val_ax[i-1]
			else:
				pass

		plot.plot(val_ax,val_or)
		plot.title(title_y_axis + '=f(' + title_x_axis + ')')
		plot.xlabel(title_x_axis)
		plot.ylabel(title_y_axis)
		plot.show()
	
	def data_save_csv(self, name, title_column1, title_column2, wv_or_time_val, abs_or_tr_or_en_val, gain_set, light_set, mode_set):			
		if os.path.exists('./data') == False:
			os.makedirs('data/')
		else:
			pass
		os.chdir('data/')
		if mode_set == '1':
			data_mode = 'Absorbance'
		elif mode_set == '2':
			data_mode = 'Transmittance'
		elif mode_set == '3':
			data_mode = 'Energy'
		else:
			pass
		
		if light_set == '1':
			light = 'WI lamp'
		elif light_set == '2':
			light = 'D2 lamp'
		elif light_set == '3':
			light = 'Custom lamp'
		else:
			pass
		print("Please type an identifier (first for raw data csv, then corrected data csv) : ")
		sample_id = input()
		filename = datetime.datetime.now().strftime("%d_%m_%Y-%H_%M_%S")
		data_file = open(sample_id + '_' +name + '_' + filename + '.csv', 'w', newline='')
		writer = csv.writer(data_file)
		writer.writerow((title_column1, title_column2))
		for val1, val2 in zip(wv_or_time_val, abs_or_tr_or_en_val) :
				writer.writerow((val1, val2))
		writer.writerow(('####', '####'))
		writer.writerow((' Gain : ', gain_set))
		writer.writerow((' Light Source : ', light))
		writer.writerow((' Mode : ', data_mode))
		writer.writerow((' Time : ', datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")))
		writer.writerow(('####', '####'))
		data_file.close()
		os.chdir('..')
		
	def data_save_csv_mono(self, name, title_column1, title_column2, wv_or_time_val, abs_or_tr_or_en_val, gain_set, light_set, mode_set):			
			if os.path.exists('./data') == False:
				os.makedirs('data/')
			else:
				pass
			os.chdir('data/')
			if mode_set == '1':
				data_mode = 'Absorbance'
			elif mode_set == '2':
				data_mode = 'Transmittance'
			elif mode_set == '3':
				data_mode = 'Energy'
			else:
				pass
			
			if light_set == '1':
				light_source = 'WI lamp'
			elif light_set == '2':
				light_source = 'D2 lamp'
			elif light_set == '3':
				light_source = 'Custom lamp'
			else:
				pass
				
			print("Please type an identifier (first for raw data csv, then corrected data csv) : ")
			sample_id_mono = input()
			filename = datetime.datetime.now().strftime("%d_%m_%Y-%H_%M_%S")
			data_file = open(sample_id_mono + '_' + name + '_' + filename + '.csv', 'w', newline='')
			writer = csv.writer(data_file)
			writer.writerow((title_column1, title_column2))

			writer.writerow((int(wv_or_time_val)/10, abs_or_tr_or_en_val))
			writer.writerow(('####', '####'))
			writer.writerow((' Gain : ', gain_set))
			writer.writerow((' Light Source : ', light_source))
			writer.writerow((' Mode : ', data_mode))
			writer.writerow((' Time : ', datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")))
			writer.writerow(('####', '####'))
			data_file.close()
			os.chdir('..')


	#def data_conv_transm_mono(self, ABS_raw):
	#	ABS_raw = float(ABS_raw)
	#	self.ABS_corr = pow(10, -ABS_raw) * 100
	#	self.ABS_corr = self.ABS_raw
	#	return self.ABS_corr
