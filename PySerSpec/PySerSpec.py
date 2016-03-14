
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
#### If something bad happens, well, in advance, sorry ! :(				####
########################### MAIN PROGRAM ###################################
############################################################################

################# Files and librairies #####################################
import serial
from send_data import SendData
from reception_data import DataReception
from connect import ConnectPort
############################################################################

print("#####################################################################")
print("PySerSpec for Shimdazu UVmini-120 UV-Vis spectrophotometer")
print("Author : Paul Bonijol")
print("#####################################################################")

############################################################################
#################### PORT SELECTION AND TEST ###############################
############################################################################
print ("################ PORT SETTINGS #####################################")
CONNECTEDPORT = ConnectPort()

while True:
	try:
		CONNECTEDPORT.get_port()
		CONNECTEDPORT.open_port()
		PORT_SET = CONNECTEDPORT.port.port
		CONNECTEDPORT.close_port()
		print("Selected port seems to be OK !")
		break
	except serial.SerialException as e2: # wrong port = exception error code 2
		print("Selected port seems not to be a working one, please define another one.")
		CONNECTEDPORT.get_port()
		
############################################################################
############################################################################



##### DEFAULT VARIABLES ####################################################
wv_set = 5500 # seems that 550 is the default for the D2 lamp
data_acc_time_set = '2' # 0.1 seconds by default ?
mode_set = '1' # absorbance
light_set = '2' # D2 lamp
gain_set = '3' # gain set to 3 by default
############################################################################
menu_choices = ["1 : Mode", "2 : Light source", "3 : Gain", "4 : Data accumulation time", "5 : Scan (single value)", 
"6 : Scan (spectrum)", "7 : Scan (time)", "8 : UNTESTED FUNCTIONS", "9 : Exit"]
end_menu_princ = ''
while end_menu_princ != 1:
	print("################ MAIN MENU ####################################")
	for i in range(9):
		print(menu_choices[int(i)])
		
	real_menu_choices = ['1','2','3','4','5','6','7','8','9']
	user_choice = ''
	while user_choice not in real_menu_choices:
		user_choice = input()
		
	if user_choice == '1':
		print ("################ MODE ####################################################")
		end_menu_mode = ''
		while end_menu_mode != '1':
			MODE = SendData()
			MODE.get_MODE_VAL()
			mode_set = MODE.MODE_VAL

			MODE.MEASUREMENTSMODE_SIGNAL1 = '\x76'
			MODE.MEASUREMENTSMODE_SIGNAL2 = str(mode_set)
			MODE.MEASUREMENTSMODE_SIGNAL3 = '\x00'
			
			MODE.port.port = str(PORT_SET)
			MODE.open_port()
			MODE.send_special(MODE.MEASUREMENTSMODE_SIGNAL1, MODE.MEASUREMENTSMODE_SIGNAL2, MODE.MEASUREMENTSMODE_SIGNAL3)
			MODE.close_port()
			print("Parameter set. Going back to main menu ...")
			break
	elif user_choice == '2':
		print("################ LIGHT SOURCE ############################################")
		print("Changing the lamp will only work while in energy mode ;")
		print("Also, lamp shutdown automatically when not in its attributed wavelength range.")
		end_menu_light = ''
		while end_menu_light != '1':
			LIGHT = SendData()
			LIGHT.get_LIGHT_VAL()
			light_set = LIGHT.LIGHT_VAL
			
			LIGHT.LIGHTSOURCETYPE_SIGNAL1 = '\x6c'
			LIGHT.LIGHTSOURCETYPE_SIGNAL2 = str(light_set)
			LIGHT.LIGHTSOURCETYPE_SIGNAL3 = '\x00'
			
			LIGHT.port.port = PORT_SET
			LIGHT.open_port()
			LIGHT.send_special(LIGHT.LIGHTSOURCETYPE_SIGNAL1, LIGHT.LIGHTSOURCETYPE_SIGNAL2, LIGHT.LIGHTSOURCETYPE_SIGNAL3)
			LIGHT.close_port()
			print("Parameter set. Going back to main menu ...")
			break

	elif user_choice == '3':
		print ("################ GAIN ####################################################")
		print("Changing the gain will only work for energy mode.")
		end_menu_gain = ''
		while end_menu_gain != '1':
			GAIN = SendData()
			GAIN.get_GAIN_VAL()
			gain_set = GAIN.GAIN_VAL

			GAIN.GAINSET_SIGNAL1 = '\x67'
			GAIN.GAINSET_SIGNAL2 = str(gain_set)
			GAIN.GAINSET_SIGNAL3 = '\x00'


			GAIN.port.port = PORT_SET
			GAIN.open_port()
			GAIN.send_special(GAIN.GAINSET_SIGNAL1, GAIN.GAINSET_SIGNAL2, GAIN.GAINSET_SIGNAL3)
			GAIN.close_port()
			print("Parameter set. Going back to main menu ...")
			break
			
	elif user_choice == '4':
		print ("################ DATA ACCUMULATION TIME ##################################")
		end_menu_dat = ''
		while end_menu_dat != '1':
			DATA_ACC_TIME = SendData()
			DATA_ACC_TIME.get_DATA_ACC_VAL()
			data_acc_time_set = DATA_ACC_TIME.DATA_ACC_VAL

			DATA_ACC_TIME.DATA_ACC_TIME_SIGNAL = ' '.join(['\x6a', str(data_acc_time_set), '\x00'])
			DATA_ACC_TIME.port.port = PORT_SET
			DATA_ACC_TIME.open_port()
			DATA_ACC_TIME.send_port(DATA_ACC_TIME.DATA_ACC_TIME_SIGNAL)
			DATA_ACC_TIME.close_port()
			print("Parameter set. Going back to main menu ...")
			break
		
############# Now the funky part ! ####################################################
		
	elif user_choice == '5':
		print ("################ MEASUREMENT (SINGLE) ####################################")
		mes_menu_choices = ["1 : Set blank", "2 : Set wavelength (standalone)", "3 : Read value", "4 : Main menu", "5 : Exit"]
		real_mes_menu_choices = ['1','2','3','4', '5']
		end_menu_mes = ''
		while end_menu_mes != 1:
			for i in range(5):
				print(mes_menu_choices[i])
			mes_menu_user_choice = ''
			while mes_menu_user_choice not in real_mes_menu_choices:
				mes_menu_user_choice = input()
			
			if mes_menu_user_choice == '1':
				print('Insert the blank sample and press enter.')
				input()
				TZ = SendData()
				TZ.port.port = PORT_SET
				TZ.get_WV_VAL()
				tz_wv = TZ.WV_VAL
				TZ.WAVELENGTHVALUE_SIGNAL = ' '.join(['\x77', str(tz_wv), '\x00'])
				TZ.open_port()	
				TZ.send_port(TZ.WAVELENGTHVALUE_SIGNAL)
				TZ.close_port()
				
				BLANK_SET = SendData()
				BLANK_SET.port.port = PORT_SET
				BLANK_SET.RESET_SIGNAL = '\x78\x00'
				BLANK_SET.open_port()
				BLANK_SET.send_port(BLANK_SET.RESET_SIGNAL)
				BLANK_SET.close_port()
				
			elif mes_menu_user_choice == '2':
				WV_SET = SendData()
				WV_SET.port.port = PORT_SET
				WV_SET.get_WV_VAL()
				wv_set = WV_SET.WV_VAL
				WV_SET.WAVELENGTHVALUE_SIGNAL = ' '.join(['\x77', str(wv_set), '\x00'])
				WV_SET.open_port()
				WV_SET.send_port(WV_SET.WAVELENGTHVALUE_SIGNAL)
				WV_SET.close_port()
				print("Going back to main menu ...")
				break
				
			elif mes_menu_user_choice == '3':
				TY_WV_SET = SendData()
				TY_WV_SET.port.port = PORT_SET
				TY_WV_SET.get_WV_VAL()
				wv_set = TY_WV_SET.WV_VAL
				TY_WV_SET.WAVELENGTHVALUE_SIGNAL = ' '.join(['\x77', str(wv_set), '\x00'])
				TY_WV_SET.open_port()
				TY_WV_SET.send_port(TY_WV_SET.WAVELENGTHVALUE_SIGNAL)
				TY_WV_SET.close_port()
					
				print("Note : in non-spectral mode, lamp choice is ruled by the spectrophotometer.")
				print('Please make sure that the blank was set first.')
				print('Insert the sample and press enter.')
				input()
				
				
				DATA_MONO = DataReception()
				DATA_MONO.SIGNAL = '\x64\x00'
				DATA_MONO.port.port = PORT_SET
				DATA_MONO.open_port()
				DATA_MONO.rec_data(DATA_MONO.SIGNAL)
				DATA_MONO.close_port()

				
				DATA_MONO.data_value(DATA_MONO.DATA_output)
				
				if mode_set == '1':
					print("Absorbance at " + str(wv_set/10) + " nm : " + str(DATA_MONO.ABS_corr))

					print("Saving data...")
					DATA_MONO.data_save_csv_mono('RAW data','Wavelength (nm)', 'Absorbance', wv_set, DATA_MONO.ABS_raw, gain_set, light_set, mode_set)
					DATA_MONO.data_save_csv_mono('Corrected data','Wavelength (nm)', 'Absorbance', wv_set, DATA_MONO.ABS_corr, gain_set, light_set, mode_set)
					print("Data saved.")
					
				elif mode_set == '2':					
					print("Transmittance at " + str(wv_set/10) + " nm : " + str(DATA_MONO.ABS_corr))
					
					print("Saving data...")
					DATA_MONO.data_save_csv_mono('RAW data','Wavelength (nm)', 'Transmittance', wv_set, DATA_MONO.ABS_raw, gain_set, light_set, mode_set)
					DATA_MONO.data_save_csv_mono('Corrected data','Wavelength (nm)', 'Transmittance', wv_set, DATA_MONO.ABS_corr, gain_set, light_set, mode_set)
					print("Data saved.")
					
				elif mode_set == '3':
					print("Energy at " + str(wv_set/10) + " nm : " + str(DATA_MONO.ABS_corr))
					print("Saving data...")
					DATA_MONO.data_save_csv_mono('RAW data','Wavelength (nm)', 'Energy', wv_set, DATA_MONO.ABS_raw, gain_set, light_set, mode_set)
					DATA_MONO.data_save_csv_mono('Corrected data','Wavelength (nm)', 'Energy', wv_set, DATA_MONO.ABS_corr, gain_set, light_set, mode_set)
					print("Data saved.")
			
			elif mes_menu_user_choice == '4':
				break
				
			elif mes_menu_user_choice == '5':
				end_menu_mes = '1'
				print("Closing now. Goodbye !")
				exit()

	elif user_choice == '6':
		print ("################ MEASUREMENTS (SPECTRUM) #######################################################")
		spectrum_menu_choices = ["1 : Set blank (baseline correction)", "2 : Set wavelength range (standalone)", "3 : Read spectrum", "4 : Main menu", "5 : Exit"]
		real_spectrum_menu_choices = ['1','2','3','4','5']
		end_menu_spectrum = ''
		while end_menu_spectrum != 1:
			for i in range(5):
				print(spectrum_menu_choices[i])
			spectrum_menu_user_choice = ''
			while spectrum_menu_user_choice not in real_spectrum_menu_choices:
				spectrum_menu_user_choice = input()
			if spectrum_menu_user_choice == '1':
					print('Baseline correction. Please keep in mind that it can take up to 10 minutes.')
					print('Insert the blank sample and press enter.')
					input()
					BASELINE_CORR = SendData()
					BASELINE_CORR.get_BASE_CORR_MAX_VAL()
					BASELINE_CORR.get_BASE_CORR_MIN_VAL()
					BASELINE_CORR.get_DIFF_VAL_BASECORR()
					while BASELINE_CORR.test_MAX_MINUS_MIN_BASECORR() != 1:
						print("Difference between MIN and MAX values should be at least 100. Please enter another set of values.")
						BASELINE_CORR.get_BASE_CORR_MAX_VAL()
						BASELINE_CORR.get_BASE_CORR_MIN_VAL()
						BASELINE_CORR.get_DIFF_VAL_BASECORR()
					min_val = BASELINE_CORR.BASE_CORR_MIN_VAL
					max_val = BASELINE_CORR.BASE_CORR_MAX_VAL
					BASELINE_CORR.BASELINECORRECTION_SIGNAL = ' '.join(['\x63', str(max_val), '\x2c', str(min_val), '\x00'])
					BASELINE_CORR.port.port = PORT_SET
					BASELINE_CORR.open_port()
					BASELINE_CORR.send_port(BASELINE_CORR.BASELINECORRECTION_SIGNAL)
					BASELINE_CORR.close_port()					
					
			elif spectrum_menu_user_choice == '2':
				input()
				SPECTRUM = SendData()
				SPECTRUM.get_SP_MAX_VAL()
				SPECTRUM.get_SP_MIN_VAL()
				SPECTRUM.get_DIFF_VAL()
				while SPECTRUM.test_MAX_MINUS_MIN() != '1':
					print("Difference between MIN and MAX values should be at least 100. Please enter another set of values.")
					SPECTRUM.get_SP_MAX_VAL()
					SPECTRUM.get_SP_MIN_VAL()
					SPECTRUM.get_DIFF_VAL()
				SPECTRUM.get_SPEED_VAL()
					
				min_val = SPECTRUM.SP_MIN_VAL
				max_val = SPECTRUM.SP_MAX_VAL
				speed_val = SPECTRUM.SPEED_VAL
				SPECTRUM.SPECTRUMSCAN_SIGNAL = ' '.join(['\x61', str(max_val), '\x2c', str(min_val), '\x2c', str(speed_val), '\x00'])
				SPECTRUM.port.port = PORT_SET
				SPECTRUM.open_port()
				SPECTRUM.send_port(SPECTRUM.SPECTRUMSCAN_SIGNAL)
				SPECTRUM.close_port()
				print("Going back to main menu ...")
				break
			
			elif spectrum_menu_user_choice == '3':
				SPECTRUM2 = SendData()
				SPECTRUM2.get_SP_MAX_VAL()
				SPECTRUM2.get_SP_MIN_VAL()
				SPECTRUM2.get_DIFF_VAL()
				while SPECTRUM2.test_MAX_MINUS_MIN() != '1':
					print("Difference between MIN and MAX values should be at least 100. Please enter another set of values.")
					SPECTRUM2.get_SP_MAX_VAL()
					SPECTRUM2.get_SP_MIN_VAL()
					SPECTRUM2.get_DIFF_VAL()
				SPECTRUM2.get_SPEED_VAL()
					
				min_val = SPECTRUM2.SP_MIN_VAL
				max_val = SPECTRUM2.SP_MAX_VAL
				speed_val = SPECTRUM2.SPEED_VAL
				SPECTRUM2.SPECTRUMSCAN_SIGNAL = ' '.join(['\x61', str(max_val), '\x2c', str(min_val), '\x2c', str(speed_val), '\x00'])
				SPECTRUM2.port.port = PORT_SET
				SPECTRUM2.open_port()
				SPECTRUM2.send_port(SPECTRUM2.SPECTRUMSCAN_SIGNAL)
				SPECTRUM2.close_port()
				
				data_points = SPECTRUM2.get_DATA_POINTS()
			
				SPECTRUM2_REC = DataReception()
				SPECTRUM2_REC.SIGNAL = ' '.join(['\x66', str(data_points), '\x00'])
				SPECTRUM2_REC.port.port = PORT_SET
				SPECTRUM2_REC.open_port()
				SPECTRUM2_REC.rec_data(SPECTRUM2_REC.SIGNAL)
				SPECTRUM2_REC.close_port()
					
				SPECTRUM2_REC.data_spectrum(SPECTRUM2_REC.DATA_output)
				
				if mode_set == '1':
					print("Saving data...")
					SPECTRUM2_REC.data_save_csv('RAW_data', 'Wavelength (nm)', 'Absorbance', SPECTRUM2_REC.WV, SPECTRUM2_REC.ABS_raw, gain_set, light_set, mode_set)
					SPECTRUM2_REC.data_save_csv('Corrected_data', 'Wavelength (nm)', 'Absorbance', SPECTRUM2_REC.WV, SPECTRUM2_REC.ABS_corr, gain_set, light_set, mode_set)
					print("Data saved.")
					
					plot_choice = ['Y', 'N']
					print("Plot corrected data ? Y/N \n")
					plot_resp = ''
					while plot_resp not in plot_choice:
						plot_resp = input()
					if plot_resp == 'Y':
						SPECTRUM2_REC.data_plot('Wavelength (nm)', 'Absorbance',SPECTRUM2_REC.WV, SPECTRUM2_REC.ABS_corr)
					elif plot_resp == 'N':
						pass
					print("Plot raw data ? Y/N \n")
					plot_resp = ''
					while plot_resp not in plot_choice:
						plot_resp = input()
					if plot_resp == 'Y':
						SPECTRUM2_REC.data_plot('Wavelength (nm)', 'Absorbance',SPECTRUM2_REC.WV, SPECTRUM2_REC.ABS_raw)
					elif plot_resp == 'N':
						pass
			
				elif mode_set == '2':
					print("Saving data...")
					SPECTRUM2_REC.data_save_csv('RAW_data','Wavelength (nm)', 'Transmittance', SPECTRUM2_REC.WV, SPECTRUM2_REC.ABS_raw, gain_set, light_set, mode_set)
					SPECTRUM2_REC.data_save_csv('Corrected_data','Wavelength (nm)', 'Transmittance', SPECTRUM2_REC.WV, SPECTRUM2_REC.ABS_corr, gain_set, light_set, mode_set)
					print("Data saved.")
					plot_choice = ['Y', 'N']
					print("Plot data ? Y/N \n")
					plot_resp = ''
					while plot_resp not in plot_choice:
						plot_resp = input()
					if plot_resp == 'Y':
						SPECTRUM2_REC.data_plot('Wavelength (nm)', 'Transmittance',SPECTRUM2_REC.WV, SPECTRUM2_REC.ABS_corr)
					elif plot_resp == 'N':
						pass
					print("Plot raw data ? Y/N \n")
					plot_resp = ''
					while plot_resp not in plot_choice:
						plot_resp = input()
					if plot_resp == 'Y':
						SPECTRUM2_REC.data_plot('Wavelength (nm)', 'Transmittance',SPECTRUM2_REC.WV, SPECTRUM2_REC.ABS_raw)
					elif plot_resp == 'N':
						pass

				elif mode_set == '3':
					print("Saving data...")
					SPECTRUM2_REC.data_save_csv('RAW_data', 'Wavelength (nm)', 'Energy', SPECTRUM2_REC.WV, SPECTRUM2_REC.ABS_raw, gain_set, light_set, mode_set)
					SPECTRUM2_REC.data_save_csv('Corrected_data','Wavelength (nm)', 'Energy', SPECTRUM2_REC.WV, SPECTRUM2_REC.ABS_corr, gain_set, light_set, mode_set)					
					print("Data saved.")
					
					plot_choice = ['Y', 'N']
					print("Plot  data ? Y/N \n")
					plot_resp = ''
					while plot_resp not in plot_choice:
						plot_resp = input()
					if plot_resp == 'Y':
						SPECTRUM2_REC.data_plot('Wavelength (nm)', 'Energy',SPECTRUM2_REC.WV, SPECTRUM2_REC.ABS_corr)
					elif plot_resp == 'N':
						pass				
					print("Plot raw data ? Y/N \n")
					plot_resp = ''
					while plot_resp not in plot_choice:
						plot_resp = input()
					if plot_resp == 'Y':
						SPECTRUM2_REC.data_plot('Wavelength (nm)', 'Energy',SPECTRUM2_REC.WV, SPECTRUM2_REC.ABS_raw)
					elif plot_resp == 'N':
						pass
			elif spectrum_menu_user_choice == '4':
				break
						
			elif spectrum_menu_user_choice == '5':
					end_menu_spectrum = '1'
					exit()
			
	elif user_choice == '7':
		print ("################ TIME SCAN #################################")
		
		TIMESCAN_TZ = SendData()
		TIMESCAN_TZ.port.port = PORT_SET
		TIMESCAN_TZ.get_WV_VAL()
		TIMESCAN_tz_wv = TIMESCAN_TZ.WV_VAL
		TIMESCAN_TZ.WAVELENGTHVALUE_SIGNAL = ' '.join(['\x77', str(TIMESCAN_tz_wv), '\x00'])
		TIMESCAN_TZ.open_port()	
		TIMESCAN_TZ.send_port(TIMESCAN_TZ.WAVELENGTHVALUE_SIGNAL)
		TIMESCAN_TZ.close_port()
		
		print("Set blank (Y/N)?")
		blank_choice = ['Y', 'N']
		blank_resp = ''
		while blank_resp not in blank_choice:
			blank_resp = input()
		if blank_resp == 'Y':
			print("Please insert the blank sample, and then press enter")
			input()
			TIMESCAN_BLANK_SET = SendData()
			TIMESCAN_BLANK_SET.port.port = PORT_SET
			TIMESCAN_BLANK_SET.RESET_SIGNAL = '\x78\x00'
			TIMESCAN_BLANK_SET.open_port()
			TIMESCAN_BLANK_SET.send_port(TIMESCAN_BLANK_SET.RESET_SIGNAL)
			TIMESCAN_BLANK_SET.close_port()
		else:
			pass
		
		print("Please insert the sample to measure, and then press enter.")
		input()
		TIMESCAN = SendData()
		TIMESCAN.port.port = PORT_SET
		TIMESCAN.get_TIME_UNIT_VAL()
		if TIMESCAN.TIME_UNIT_VAL == 0:
			TIMESCAN.get_TIME_RANGE()
			time_range = TIMESCAN.TIME_RANGE
		else:
			time_range = 2
			pass
		
		TIMESCAN.get_TIME_VAL()
		TIMESCAN.get_TIME_POINTS()
		time_val = TIMESCAN.TIME_VAL
		time_unit_val = TIMESCAN.TIME_UNIT_VAL
		time_points = TIMESCAN.TIME_DATA_POINTS
		TIMESCAN.TIMESCAN_SIGNAL = ' '.join(['\x62', str(time_val), '\x2c', str(time_unit_val), '\x00'])
		TIMESCAN.open_port()
		TIMESCAN.send_port(TIMESCAN.TIMESCAN_SIGNAL)
		TIMESCAN.close_port()
		
		TIMESCAN_REC = DataReception()
		TIMESCAN_REC.SIGNAL = ' '.join(['\x66', str(time_points), '\x00'])
		TIMESCAN_REC.port.port = PORT_SET
		TIMESCAN_REC.open_port()
		TIMESCAN_REC.rec_data(TIMESCAN_REC.SIGNAL)
		TIMESCAN_REC.close_port()
		if time_range == 1:
			TIMESCAN_REC.data_time_range1(TIMESCAN_REC.DATA_output)
		elif time_range == 2:
			TIMESCAN_REC.data_time_range2(TIMESCAN_REC.DATA_output)
		elif time_range == 3:
			TIMESCAN_REC.data_time_range3(TIMESCAN_REC.DATA_output, time_val)
		elif time_range == 4:
			TIMESCAN_REC.data_time_range4(TIMESCAN_REC.DATA_output, time_val)
		else:
			pass
		
		if time_unit_val == 1:
			if mode_set == '1':
				print("Saving data...")
				TIMESCAN_REC.data_save_csv('RAW data','Time (minutes)', 'Absorbance', TIMESCAN_REC.TIME, TIMESCAN_REC.ABS_raw, gain_set, light_set, mode_set)
				TIMESCAN_REC.data_save_csv('Corrected data','Time (minutes)', 'Absorbance', TIMESCAN_REC.TIME, TIMESCAN_REC.ABS_corr, gain_set, light_set, mode_set)
				print("Data saved.")
				plot_choice = ['Y', 'N']
				print("Plot corrected data ? Y/N \n")
				plot_resp = ''
				while plot_resp not in plot_choice:
					plot_resp = input()
				if plot_resp == 'Y':
					TIMESCAN_REC.data_plot('Time (minutes)', 'Absorbance',TIMESCAN_REC.TIME, TIMESCAN_REC.ABS_corr)
				elif plot_resp == 'N':
					pass
				print("Plot raw data ? Y/N \n")
				plot_resp = ''
				while plot_resp not in plot_choice:
					plot_resp = input()
				if plot_resp == 'Y':
					TIMESCAN_REC.data_plot('Time (minutes)', 'Absorbance',TIMESCAN_REC.TIME, TIMESCAN_REC.ABS_raw)
				elif plot_resp == 'N':
					pass
					
			elif mode_set == '2':
				print("Saving data...")
				TIMESCAN_REC.data_save_csv('RAW data','Time (minutes)', 'Transmittance', TIMESCAN_REC.TIME, TIMESCAN_REC.ABS_raw, gain_set, light_set, mode_set)
				TIMESCAN_REC.data_save_csv('Corrected data','Time (minutes)', 'Transmittance', TIMESCAN_REC.TIME, TIMESCAN_REC.ABS_corr, gain_set, light_set, mode_set)
				print("Data saved.")
				
				plot_choice = ['Y', 'N']
				print("Plot corrected data ? Y/N \n")
				plot_resp = ''
				while plot_resp not in plot_choice:
					plot_resp = input()
				if plot_resp == 'Y':
					TIMESCAN_REC.data_plot('Time (minutes)', 'Transmittance',TIMESCAN_REC.TIME, TIMESCAN_REC.ABS_corr)
				elif plot_resp == 'N':
					pass
				print("Plot raw data ? Y/N \n")
				plot_resp = ''
				while plot_resp not in plot_choice:
					plot_resp = input()
				if plot_resp == 'Y':
					TIMESCAN_REC.data_plot('Time (minutes)', 'Transmittance',TIMESCAN_REC.TIME, TIMESCAN_REC.ABS_raw)
				elif plot_resp == 'N':
					pass
					
			elif mode_set == '3':
				print("Saving data...")
				TIMESCAN_REC.data_save_csv('RAW data','Time (minutes)', 'Energy', TIMESCAN_REC.TIME, TIMESCAN_REC.ABS_raw, gain_set, light_set, mode_set)
				TIMESCAN_REC.data_save_csv('Corrected data','Time (minutes)', 'Energy', TIMESCAN_REC.TIME, TIMESCAN_REC.ABS_corr, gain_set, light_set, mode_set)					
				print("Data saved.")
				
				plot_choice = ['Y', 'N']
				print("Plot corrected data ? Y/N \n")
				plot_resp = ''
				while plot_resp not in plot_choice:
					plot_resp = input()
				if plot_resp == 'Y':
					TIMESCAN_REC.data_plot('Time (minutes)', 'Energy',TIMESCAN_REC.TIME, TIMESCAN_REC.ABS_corr)
				elif plot_resp == 'N':
					pass
				print("Plot raw data ? Y/N \n")
				plot_resp = ''
				while plot_resp not in plot_choice:
					plot_resp = input()
				if plot_resp == 'Y':
					TIMESCAN_REC.data_plot('Time (minutes)', 'Energy',TIMESCAN_REC.TIME, TIMESCAN_REC.ABS_raw)
				elif plot_resp == 'N':
					pass
					
		elif time_unit_val == 0:
			if mode_set == '1':
				print("Saving data...")
				TIMESCAN_REC.data_save_csv('RAW data','Time (seconds)', 'Absorbance', TIMESCAN_REC.TIME*10, TIMESCAN_REC.ABS_raw, gain_set, light_set, mode_set)
				TIMESCAN_REC.data_save_csv('Corrected data','Time (seconds)', 'Absorbance', TIMESCAN_REC.TIME*10, TIMESCAN_REC.ABS_corr, gain_set, light_set, mode_set)
				print("Data saved.")
				
				plot_choice = ['Y', 'N']
				print("Plot corrected data ? Y/N \n")
				plot_resp = ''
				while plot_resp not in plot_choice:
					plot_resp = input()
				if plot_resp == 'Y':
					TIMESCAN_REC.data_plot('Time (seconds)', 'Absorbance',TIMESCAN_REC.TIME, TIMESCAN_REC.ABS_corr)
				elif plot_resp == 'N':
					pass
				print("Plot raw data ? Y/N \n")
				plot_resp = ''
				while plot_resp not in plot_choice:
					plot_resp = input()
				if plot_resp == 'Y':
					TIMESCAN_REC.data_plot('Time (seconds)', 'Absorbance',TIMESCAN_REC.TIME, TIMESCAN_REC.ABS_raw)
				elif plot_resp == 'N':
					pass
					
			elif mode_set == '2':
				print("Saving data...")
				TIMESCAN_REC.data_save_csv('RAW data','Time (seconds)', 'Transmittance', TIMESCAN_REC.TIME*10, TIMESCAN_REC.ABS_raw, gain_set, light_set, mode_set)
				TIMESCAN_REC.data_save_csv('Corrected data','Time (seconds)', 'Transmittance', TIMESCAN_REC.TIME*10, TIMESCAN_REC.ABS_corr, gain_set, light_set, mode_set)
				print("Data saved.")
				
				plot_choice = ['Y', 'N']
				print("Plot corrected data ? Y/N \n")
				plot_resp = ''
				while plot_resp not in plot_choice:
					plot_resp = input()
				if plot_resp == 'Y':
					TIMESCAN_REC.data_plot('Time (seconds)', 'Transmittance', TIMESCAN_REC.TIME, TIMESCAN_REC.ABS_corr)
				elif plot_resp == 'N':
					pass
				print("Plot raw data ? Y/N \n")
				plot_resp = ''
				while plot_resp not in plot_choice:
					plot_resp = input()
				if plot_resp == 'Y':
					TIMESCAN_REC.data_plot('Time (seconds)', 'Transmittance',TIMESCAN_REC.TIME, TIMESCAN_REC.ABS_raw)
				elif plot_resp == 'N':
					pass
					
			elif mode_set == '3':
				print("Saving data...")
				TIMESCAN_REC.data_save_csv('RAW data','Time (seconds)', 'Energy', TIMESCAN_REC.TIME*10, TIMESCAN_REC.ABS_raw, gain_set, light_set, mode_set)
				TIMESCAN_REC.data_save_csv('Corrected data','Time (seconds)', 'Energy', TIMESCAN_REC.TIME*10, TIMESCAN_REC.ABS_corr, gain_set, light_set, mode_set)					
				print("Data saved.")
				
				plot_choice = ['Y', 'N']
				print("Plot corrected data ? Y/N \n")
				plot_resp = ''
				while plot_resp not in plot_choice:
					plot_resp = input()
				if plot_resp == 'Y':
					TIMESCAN_REC.data_plot('Time (seconds)', 'Energy',TIMESCAN_REC.TIME, TIMESCAN_REC.ABS_corr)
				elif plot_resp == 'N':
					pass
				print("Plot raw data ? Y/N \n")
				plot_resp = ''
				while plot_resp not in plot_choice:
					plot_resp = input()
				if plot_resp == 'Y':
					TIMESCAN_REC.data_plot('Time (seconds)', 'Energy',TIMESCAN_REC.TIME, TIMESCAN_REC.ABS_raw)
				elif plot_resp == 'N':
					pass
		
		else:
			print("bug")
	elif user_choice == '8':
		print ("################ UNTESTED FUNCTIONS ########################################################################")
		specfunc_menu_choices = ["1 : Multi-cell / CPS-240 holder","2 : Sipper","3 : Read ASC nozzle state", "4 : Main Menu", "5 : Exit"]
		real_specfunc_menu_choices = ['1','2','3','4', '5']
		end_menu_specfunc = ''
		while end_menu_specfunc != 1:
			for i in range(5):
				print(specfunc_menu_choices[i])
			specfunc_menu_user_choice = ''
			while specfunc_menu_user_choice not in real_specfunc_menu_choices:
				specfunc_menu_user_choice = input()
			
			if specfunc_menu_user_choice == '1':
				
				print ("################ MULTI-CELL / CPS-240 HOLDER ###################################################")
				mc_menu_choices = ["1 : Multi-cell type","2 : Move cuvette forward","3 : Move cuvette backward (CPS-240) or return to position 1 (multi-cell holder)","4 : Check cuvette position","5 : Previous menu","6 : Exit"]
				real_mc_menu_choices = ['1','2','3','4','5', '6']
				end_menu_mc = ''
				while end_menu_mc != 1:
					for i in range(6):
						print(mc_menu_choices[i])
					mc_menu_user_choice = ''
					while mc_menu_user_choice not in real_mc_menu_choices:
						mc_menu_user_choice = input()
					if mc_menu_user_choice == '1':
						print("Please select the sample holder type : \n")
						CUVETTE_TYPE_choice = ["1 : Standard", "2 : 6 positions", "3 : CPS-240"]
						for i in CUVETTE_TYPE_choice:
							print(i)
						real_CUVETTE_TYPE_choice = ['1','2','3']
						CUVETTE_TYPE_user_choice = ''
						while CUVETTE_TYPE_user_choice not in real_CUVETTE_TYPE_choice:
							CUVETTE_TYPE_user_choice = input()
							
						if CUVETTE_TYPE_user_choice == '1':
							CUVETTE = '\x6d\x31\x00'
							
						elif CUVETTE_TYPE_user_choice == '2':
							CUVETTE = '\x6d\x32\x00'
							
						elif CUVETTE_TYPE_user_choice == '3':
							CUVETTE = '\x6d\x31\x30\x00'
						
						CUVETTE_TYPE = SendData()
						CUVETTE_TYPE.SIGNAL = CUVETTE
						CUVETTE_TYPE.port.port = PORT_SET
						CUVETTE_TYPE.open_port()
						CUVETTE_TYPE.send_port(CUVETTE_TYPE.SIGNAL)
						CUVETTE_TYPE.close_port()
						print("Sample holder type set.")
						
					elif mc_menu_user_choice == '2':
						CUVETTE_MOVE_FW = SendData()
						CUVETTE_MOVE_FW.SIGNAL = '\x71\x31\x00'
						CUVETTE_MOVE_FW.port.port = PORT_SET
						CUVETTE_MOVE_FW.open_port()
						CUVETTE_MOVE_FW.send_port(CUVETTE_MOVE_FW.SIGNAL)
						CUVETTE_MOVE_FW.close_port()
						print("Cuvette moved forward.")
						
					elif mc_menu_user_choice == '3':
						CUVETTE_MOVE_BW = SendData()
						CUVETTE_MOVE_BW.SIGNAL = '\x71\x32\x00'
						CUVETTE_MOVE_BW.port.port = PORT_SET
						CUVETTE_MOVE_BW.open_port()
						CUVETTE_MOVE_BW.send_port(CUVETTE_MOVE_BW.SIGNAL)
						CUVETTE_MOVE_BW.close_port()
						print("Cuvette moved backward (CPS-240) / returned to position 1 (multi-cell holder).")
						
					elif mc_menu_user_choice == '4':
						CUVETTE_CHECK_POSITION = DataReception()
						CUVETTE_CHECK_POSITION.SIGNAL = '\x71\x00'
						CUVETTE_CHECK_POSITION.port.port = PORT_SET
						CUVETTE_CHECK_POSITION.open_port()
						CUVETTE_CHECK_POSITION.rec_data(CUVETTE_CHECK_POSITION.SIGNAL)
						CUVETTE_CHECK_POSITION.get_CUVETTE_POS(CUVETTE_CHECK_POSITION.DATA_output)
					
					elif mc_menu_user_choice == '5':		
						break
					
					elif mc_menu_user_choice == '6':		
						print("Closing now. Goodbye !")
						end_menu_mc = '1'
						end_menu_specfunc = '1'
						exit()
			
			
			elif specfunc_menu_user_choice == '2':
				print ("################ SIPPER #################################################################################")
				sip_menu_choices = ["1 : Sipper 160 controls", "2 : Seringe sipper controls","3 : Seringe sipper light ON","4 : Seringe sipper light OFF","5 : Previous menu","6 : Exit"]
				real_sip_menu_choices = ['1','2','3','4','5', '6']
				end_menu_sip = ''
				while end_menu_sip != 1:
					for i in range(6):
						print(sip_menu_choices[i])
					sip_menu_user_choice = ''
					while sip_menu_user_choice not in real_sip_menu_choices:
						sip_menu_user_choice = input()
						
					if sip_menu_user_choice == '1':
						SIPPER160 = SendData()
						SIPPER160.port.port = PORT_SET
						SIPPER160.get_SIPPER160_PARAMS()
						mode_val = SIPPER160.SIPPER160_MODE
						speed_val = SIPPER160.SIPPER160_MODE
						time_val = SIPPER160.SIPPER160_MODE
						SIPPER160.SIPPER160_SIGNAL = ' '.join(['\x70', str(mode_val), '\x2c', str(speed_val), '\x2c', str(time_val), '\x00'])
						SIPPER160.open_port()
						SIPPER160.send_port(SIPPER160.SIPPER160_SIGNAL)
						SIPPER160.close_port()
						print("Sipper 160 configured.")
						
					elif sip_menu_user_choice == '2':
						SIPPER_SER = SendData()
						SIPPER_SER.port.port = PORT_SET
						SIPPER_SER.get_SERINGESIPPER_PARAMS()
						mode_ser_val = SIPPER_SER.SIPPERSERINGE_MODE
						speed_ser_val = SIPPER_SER.SIPPERSERINGE_SPEED
						capacity_ser_val = SIPPER_SER.SIPPERSERINGE_CAPACITY
						
						SIPPER_SER.SIPPER_SER_SIGNAL = ' '.join(['\x6f', str(mode_ser_val), '\x2c', str(speed_ser_val), '\x2c', str(capacity_ser_val), '\x00'])
						SIPPER_SER.open_port()
						SIPPER_SER.send_port(SIPPER_SER.SIPPER_SER_SIGNAL)
						SIPPER_SER.close_port()
						print("Seringe sipper configured.")
					elif sip_menu_user_choice == '3':
						SIPPER_LAMP_ON = SendData()
						SIPPER_LAMP_ON.port.port = PORT_SET
						SIPPER_LAMP_ON.SIGNAL = '\x73\x31\x00'
						SIPPER_LAMP_ON.open_port()
						SIPPER_LAMP_ON.send_port(SIPPER_LAMP_ON.SIGNAL)
						SIPPER_LAMP_ON.close_port()
						print("Seringe sipper light ON.")
							
					elif sip_menu_user_choice == '4':
						SIPPER_LAMP_OFF = SendData()
						SIPPER_LAMP_OFF.port.port = PORT_SET
						SIPPER_LAMP_OFF.SIGNAL = '\x73\x30\x00'
						SIPPER_LAMP_OFF.open_port()
						SIPPER_LAMP_OFF.send_port(SIPPER_LAMP_OFF.SIGNAL)
						SIPPER_LAMP_OFF.close_port()
						print("Seringe sipper light OFF.")
					
					elif sip_menu_user_choice == '5':
						end_menu_sip = '1'
						break
						
				
					elif sip_menu_user_choice == '6':
						print("Closing now. Goodbye !")
						end_menu_sip = '1'
						end_menu_specfunc = '1'
						exit()
				
			elif specfunc_menu_user_choice == '3':
				NOZZLE = DataReception()
				NOZZLE.ASC_NOZZLE_SIGNAL = '\x72\x00'
				NOZZLE.port.port = PORT_SET
				NOZZLE.open_port()
				NOZZLE.rec_data(NOZZLE.ASC_NOZZLE_SIGNAL)
				NOZZLE.close_port()
				NOZZLE.get_ASC_POS(NOZZLE.DATA_output)
			
			elif specfunc_menu_user_choice == '4':
				break
				
			elif specfunc_menu_user_choice == '5':
				print("Closing now. Goodbye !")
				end_menu_specfunc = '1'
				exit()
			
	elif user_choice == '9':
		print("Closing now. Goodbye !")
		end_menu_princ = '1'
		exit()		
		
	else:
		print("ERROR ! Program will stop now...")
		end_menu_princ = '1'
		exit()

############################################################################
############################################################################
