

####
#TODO
# fonction définition temps attente
#Corriger import valeurs et réciprocité champ !
#Tester liste envoi et suppression
####
### macros : faire macro ridge (roi, boost contraste ou détection contour) et orientation (intégrer direct. polygone+recallage)

#-*- coding: UTF-8 -*

################################################################################################
############################### PYWRITERCONTROL ################################################
################################################################################################

# Version : 1.0
# Author : Paul Bonijol // https://github.com/paulbnjl
# License : GNU/GPL v3
# May 2016

# The purpose of this program is to allow  technicians using
# Thermo SlideWriter and Carousel MicroWriter to continue
# using these machines. Thermo won't support them anymore
# and the current application (Shandon Microwriter) is
# not working properly.

# This software use Python, PySerial and other things (tk, ttk, collections, time, datetime, os, weakref)
# that are probably included in any basic python installation (except for pyserial).
# If it's not, please be sure that everything is set up before launching
# the software.
# You can always install pythonic depencencies by using your favorite
# package manager (GNU/Linux : APT, RPM...), or pip (every OS ; pip install ###)

# Fields name are defined in this file. All was made specifically to ease the
# work of histology technicians at NAMSA Lyon.  Feel free to modify everything
# to repurpose to your own needs !

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

################################################################################################
################################################################################################
################################################################################################

################################################################################################
###################################### LIBRARIES AND IMPORTS ###################################
################################################################################################

from intf_widgets import (Interface_ComboBox, Interface_ListBox, Interface_EntryBox,
 Interface_RadioBox, Interface_ComboBoxCST, Interface_ComboBoxSDL, Interface_CheckBox)
from com_funcs import PortFunctions, ConnectPort
from itf_wait_list import Interface_WaitingList
from itf_wt_set import Interface_TimeSetWindow
from pywritercontrol_funcs import Special_Functions

################################################################################################

import tkinter as tk
import tkinter.ttk as ttk
import os
from threading import Thread
import multiprocessing
import time

################################################################################################
################################################################################################
################################################################################################

################################################################################################
###################################### INTERFACE DEFINITION ####################################
################################################################################################

# This file contain just the class call for the Tkinter elements used by the interface.
# All the backend work is made by functions defined in pywritercontrol_funcs.py.
# The serial communication functions, using pyserial, are defined in another file, com_funcs.py.
# Intf_widgets.py contain the widget definitions of all of the tkinter tk/ttk widgets called here.
# Finally, the waiting list is defined separatly, in itf_wait_list.py.

### Main Window ###
main_window = tk.Tk()
main_window.title("PyWriterControl 3.0 for THERMO slide/cassette MicroWriter")
## Main menu
barre_menu = tk.Menu(main_window)
# Frame, left
frame_left = tk.Frame(main_window, padx=5, pady=5)
# Subframe 1 : Parameters
subframe_1 = tk.LabelFrame(frame_left, text="Paramètres de gravure", padx=5, pady=5)
# Subframe 2 : entries
subframe_2 = tk.LabelFrame(frame_left, text="Saisie", padx=5, pady=5)
# Subframe 3 : load/save buttons
subframe_3 = tk.Frame(frame_left, padx=5, pady=5)
## Mainframe RIGHT
frame_right = tk.Frame(main_window, padx=5, pady=5)
# Subframe 4 : Label organisation (notebook, two tabs : one for cassettes, one for slides)
subframe_4 = ttk.Notebook(frame_right, name="disposition")
subframe_4_tab1 = tk.Frame(subframe_4)
subframe_4.add(subframe_4_tab1, text='Cassette')
subframe_4_tab2 = tk.Frame(subframe_4)
subframe_4.add(subframe_4_tab2, text='Lame')
# Subframe 5 : send to waiting list button
subframe_5 = tk.Frame(frame_right)
# Subframe 6 : Waiting queue
subframe_6 = tk.LabelFrame(frame_right, text="Liste d'attente", padx=5, pady=5)
# Subframe 7 : Buttons
subframe_7 = tk.LabelFrame(frame_right, text="Commandes", padx=5, pady=5)


################################################################################################
################################################################################################
################################################################################################


################################################################################################
########################### A STUPID, USELESS, AND THUS AWSESOME, FUNCTIONNALITY #############################
################################################################################################

# A set of useless functions made to please the technicians here
# It just allows to change the background color of the main interface.

bg_default = main_window.cget("bg")

def set_color_blue():
	main_window.configure(background='SkyBlue2')
	barre_menu.configure(background='SkyBlue2')
	frame_left.configure(background='SkyBlue2')
	subframe_1.configure(background='SkyBlue2')
	subframe_2.configure(background='SkyBlue2')
	subframe_3.configure(background='SkyBlue2')
	frame_right.configure(background='SkyBlue2')
	subframe_4_tab1.configure(background='SkyBlue2')
	subframe_4_tab2.configure(background='SkyBlue2')
	subframe_5.configure(background='SkyBlue2')
	subframe_6.configure(background='SkyBlue2')
	subframe_7.configure(background='SkyBlue2')
	
def set_color_pink():
	main_window.configure(background='LightPink1')
	barre_menu.configure(background='LightPink1')
	frame_left.configure(background='LightPink1')
	subframe_1.configure(background='LightPink1')
	subframe_2.configure(background='LightPink1')
	subframe_3.configure(background='LightPink1')
	subframe_4_tab1.configure(background='LightPink1')
	subframe_4_tab2.configure(background='LightPink1')
	frame_right.configure(background='LightPink1')
	subframe_5.configure(background='LightPink1')
	subframe_6.configure(background='LightPink1')
	subframe_7.configure(background='LightPink1')
	
def set_color_green():
	main_window.configure(background='DarkOliveGreen1')
	barre_menu.configure(background='DarkOliveGreen1')
	frame_left.configure(background='DarkOliveGreen1')
	subframe_1.configure(background='DarkOliveGreen1')
	subframe_2.configure(background='DarkOliveGreen1')
	subframe_3.configure(background='DarkOliveGreen1')
	subframe_4_tab1.configure(background='DarkOliveGreen1')
	subframe_4_tab2.configure(background='DarkOliveGreen1')	
	frame_right.configure(background='DarkOliveGreen1')
	subframe_5.configure(background='DarkOliveGreen1')
	subframe_6.configure(background='DarkOliveGreen1')
	subframe_7.configure(background='DarkOliveGreen1')
	
def set_color_orange():
	main_window.configure(background='sienna1')
	barre_menu.configure(background='sienna1')
	frame_left.configure(background='sienna1')
	subframe_1.configure(background='sienna1')
	subframe_2.configure(background='sienna1')
	subframe_3.configure(background='sienna1')
	subframe_4_tab1.configure(background='sienna1')
	subframe_4_tab2.configure(background='sienna1')	
	frame_right.configure(background='sienna1')
	subframe_5.configure(background='sienna1')
	subframe_6.configure(background='sienna1')
	subframe_7.configure(background='sienna1')

def set_color_yellow():
	main_window.configure(background='LightGoldenrod1')
	barre_menu.configure(background='LightGoldenrod1')
	frame_left.configure(background='LightGoldenrod1')
	subframe_1.configure(background='LightGoldenrod1')
	subframe_2.configure(background='LightGoldenrod1')
	subframe_3.configure(background='LightGoldenrod1')
	subframe_4_tab1.configure(background='LightGoldenrod1')
	subframe_4_tab2.configure(background='LightGoldenrod1')	
	frame_right.configure(background='LightGoldenrod1')
	subframe_5.configure(background='LightGoldenrod1')
	subframe_6.configure(background='LightGoldenrod1')
	subframe_7.configure(background='LightGoldenrod1')

def set_color_none():
	main_window.configure(background=bg_default)
	barre_menu.configure(background=bg_default)
	frame_left.configure(background=bg_default)
	subframe_1.configure(background=bg_default)
	subframe_2.configure(background=bg_default)
	subframe_3.configure(background=bg_default)
	subframe_4_tab1.configure(background=bg_default)
	subframe_4_tab2.configure(background=bg_default)
	frame_right.configure(background=bg_default)
	subframe_5.configure(background=bg_default)
	subframe_6.configure(background=bg_default)
	subframe_7.configure(background=bg_default)

			
################################################################################################
##################################### FUNCTIONS INSTANCIATION ##################################
################################################################################################
Special_Functions = Special_Functions(main_window)
waitinglist = Interface_WaitingList(subframe_6, 'waitinglist')
radiobuttons_blade_slide = Interface_RadioBox(subframe_1, 'radiobuttons_blade_slide')


################################################################################################
################################################################################################
################################################################################################

################################################################################################
###################################### MAIN MENU ###############################################
################################################################################################

# Class declarations
menu_listbox_studies = Interface_ListBox('menu_listbox_studies')
menu_listbox_delay = Interface_ListBox('menu_listbox_delay')
menu_listbox_animal_number = Interface_ListBox('menu_listbox_animal_number')
menu_listbox_animal_gender = Interface_ListBox('menu_listbox_animal_gender')
menu_listbox_group = Interface_ListBox('menu_listbox_group')
menu_listbox_organs = Interface_ListBox('menu_listbox_organs')
menu_listbox_rank = Interface_ListBox('menu_listbox_rank')
menu_listbox_animaltype = Interface_ListBox('menu_listbox_animaltype')
menu_listbox_colorations = Interface_ListBox('menu_listbox_colorations')

menu_time_set = Interface_TimeSetWindow('menu_time_set')

# Menus
menu_fichier = tk.Menu(barre_menu, tearoff = 0)

barre_menu.add_cascade(label = "Fichier", menu = menu_fichier)
menu_fichier.add_command(label = "Quitter", command = exit)

menu_edition = tk.Menu(barre_menu, tearoff = 0)

barre_menu.add_cascade(label="Edition", menu = menu_edition)

menu_listbox_studies.listbox_call("Numéros d'études", 'study_number')
menu_edition.add_command(label="Entrées numéros d'études", command = menu_listbox_studies.listbox)

menu_listbox_delay.listbox_call("Délais", 'time_schedule')
menu_edition.add_command(label="Entrées délais", command = menu_listbox_delay.listbox)

menu_listbox_animal_number.listbox_call("Numéros animaux", 'animal_number')
menu_edition.add_command(label="Entrées numéros animaux", command = menu_listbox_animal_number.listbox)

menu_listbox_animal_gender.listbox_call("Genres animaux", 'animal_gender')
menu_edition.add_command(label="Entrées genres", command = menu_listbox_animal_gender.listbox)

menu_listbox_group.listbox_call("Groupes", 'group')
menu_edition.add_command(label="Entrées groupe animaux", command = menu_listbox_group.listbox)

menu_listbox_organs.listbox_call("Organes", 'organs')
menu_edition.add_command(label="Entrées organes", command = menu_listbox_organs.listbox)

menu_listbox_rank.listbox_call("Rang", 'rank')
menu_edition.add_command(label="Entrées rang de coupe", command = menu_listbox_rank.listbox)

menu_listbox_colorations.listbox_call("Colorations", 'coloration')
menu_edition.add_command(label="Entrées colorations", command = menu_listbox_colorations.listbox)

menu_listbox_animaltype.listbox_call("Espèces", 'animal_type')
menu_edition.add_command(label="Entrées espèces", command = menu_listbox_animaltype.listbox)



menu_div = tk.Menu(barre_menu, tearoff = 0)
barre_menu.add_cascade(label="Divers", menu = menu_div)
menu_div.add_command(label="Réglages des temps de gravure", command = menu_time_set.timewindow)
menu_div.add_command(label="Interface : bleue", command = set_color_blue)
menu_div.add_command(label="Interface : rose", command = set_color_pink)
menu_div.add_command(label="Interface : vert", command = set_color_green)
menu_div.add_command(label="Interface : orange", command = set_color_orange)
menu_div.add_command(label="Interface : jaune", command = set_color_yellow)
menu_div.add_command(label="Interface : normale", command = set_color_none)

################################################################################################
################################################################################################
################################################################################################

################################################################################################
###################################### DATE AND TIME WIDGET ####################################
################################################################################################

datetime_label = tk.Label(subframe_1, text="Date : ").grid(row=0,column=0)
datetime_label = tk.Label(subframe_1, text=Special_Functions.get_time(),
 font=('Arial', 10)).grid(row=0,column=1)

################################################################################################
###################################### FIELDS ##################################################
################################################################################################

# Class declarations, comboboxes and entryboxes
port_number_cassette = Interface_ComboBox(subframe_1, 'port_number_cassette')
port_number_slidewriter = Interface_ComboBox(subframe_1, 'port_number_slidewriter')
hopper_number = Interface_ComboBox(subframe_1, 'hopper_number')
object_number = Interface_ComboBox(subframe_1, 'object_number')
animal_type = Interface_ComboBox(subframe_2, 'animal_type')
study_number = Interface_ComboBox(subframe_2, 'study_number')
time_sched = Interface_ComboBox(subframe_2, 'time_sched')
group = Interface_ComboBox(subframe_2, 'group')
gender = Interface_ComboBox(subframe_2, 'gender')
organs = Interface_ComboBox(subframe_2, 'organs')
coloration = Interface_ComboBox(subframe_2, 'coloration')
rank = Interface_ComboBox(subframe_2, 'rank')
animal_number = Interface_ComboBox(subframe_2, 'animal_number')

profile_name = Interface_EntryBox(subframe_1, 'profile_name')
sup_data1 = Interface_EntryBox(subframe_2, 'sup_data1')
sup_data2 = Interface_EntryBox(subframe_2, 'sup_data2')
sup_data3 = Interface_EntryBox(subframe_2, 'sup_data3')
sup_data4 = Interface_EntryBox(subframe_2, 'sup_data4')

# Specific checkbox to allow sending twice the command
# Simplify the process in case of two colorations (HES, TM) are made
hes_and_trichrome_option = Interface_CheckBox(subframe_5, 'hes_and_trichrome_option')


# Boxes : port, objects number, hopper, profile name
port_number_cassette.combo_ro("Port série graveur de cassettes : ", 'P', 0,1,0,1,1)
port_number_slidewriter.combo_ro("Port série graveur de lames : ", "P", 2,2,0,2,1)
hopper_number.combo_ro("Réservoir (hopper) : ", 'H', 0,3,0,3,1)
object_number.combo_ro("Nombre de cassettes/lames à marquer : ", 'O', 0,4,0,4,1)
profile_name.entry_free("Nom du profil : ",5,0,5,1)

# RadioButtons
radiobuttons_blade_slide.radiobox("Cassette(s)", "Lame(s)", "Cassette(s)+Lame(s)", 6,0)

# Labels
tk.Label(subframe_2, text="Valeur").grid(row=0,column=1)
tk.Label(subframe_2, text="Taille texte").grid(row=0,column=2)
tk.Label(subframe_2, text="Incrémenter").grid(row=0,column=3)


# Comboboxes : text fields
study_number.combo_rw("Numéro d'étude : ",'study_number',0,1,0,1,1)
study_number.combo_txt('T', 4,1,4,1,2)
study_number.box_txt.configure(width=10)
study_number.checkbox(1,3)

time_sched.combo_rw("Délai : ",'time_schedule',0,2,0,2,1)
time_sched.combo_txt('T', 4,2,4,2,2)
time_sched.box_txt.configure(width=10)
time_sched.checkbox(2,3)

animal_number.combo_rw("Numéro animal : ", "animal_number", 0,3,0,3,1)
animal_number.combo_txt('T', 4,3,4,3,2)
animal_number.box_txt.configure(width=10)
animal_number.checkbox(3,3)

gender.combo_rw("Genre : ",'animal_gender',0,4,0,4,1)
gender.combo_txt('T', 4,4,4,4,2)
gender.box_txt.configure(width=10)
gender.checkbox(4,3)

group.combo_rw("Groupe : ",'group',0,5,0,5,1)
group.combo_txt('T', 4,5,4,5,2)
group.box_txt.configure(width=10)
group.checkbox(5,3)

organs.combo_rw("Organe(s) : ", 'organs',0,6,0,6,1)
organs.combo_txt('T', 4,6,4,6,2)
organs.box_txt.configure(width=10)
organs.checkbox(6,3)

rank.combo_rw("Rang : ", 'rank',0,7,0,7,1)
rank.combo_txt('T', 4,7,4,7,2)
rank.box_txt.configure(width=10)
rank.checkbox(7,3)

coloration.combo_rw("Coloration : ", 'coloration',0,8,0,8,1)
coloration.combo_txt('T', 4,8,4,8,2)
coloration.box_txt.configure(width=10)
coloration.checkbox(8,3)

animal_type.combo_rw("Espèce : ",'animal_type',0,9,0,9,1)
animal_type.combo_txt('T', 4,9,4,9,2)
animal_type.box_txt.configure(width=10)
animal_type.checkbox(9,3)

# Entryboxes : free text
sup_data1.entry_free("Champ libre (1) : ",12,0,12,1)
sup_data1.combo_txt('T', 4,12,4,12,2)
sup_data1.box_txt.configure(width=10)
sup_data1.checkbox(12,3)

sup_data2.entry_free("Champ libre (2) : ",13,0,13,1)
sup_data2.combo_txt('T', 4,13,4,13,2)
sup_data2.box_txt.configure(width=10)
sup_data2.checkbox(13,3)

sup_data3.entry_free("Champ libre (3) : ",14,0,14,1)
sup_data3.combo_txt('T', 4,14,4,14,2)
sup_data3.box_txt.configure(width=10)
sup_data3.checkbox(14,3)

sup_data4.entry_free("Champ libre (4) : ",15,0,15,1)
sup_data4.combo_txt('T', 4,15,4,15,2)
sup_data4.box_txt.configure(width=10)
sup_data4.checkbox(15,3)

tk.Label(subframe_5, text="HES + trichrome ?").grid(row=0,column=0)
hes_and_trichrome_option.checkbox(0,1)

################################################################################################
################################################################################################
################################################################################################

################################################################################################
################################ LABEL ORGANISATION ############################################
################################################################################################

# Labels for cassettes and slides are organised
# as a grid, each element of the grid being an independent entry
# If a field is leaved empty, it is count as a 'space' between
# the two nearest fields

# Class declarations
cassettelabel_field1 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field1")
cassettelabel_field2 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field2")
cassettelabel_field3 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field3")
cassettelabel_field4 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field4")
cassettelabel_field5 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field5")
cassettelabel_field6 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field6")
cassettelabel_field7 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field7")
cassettelabel_field8 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field8")
cassettelabel_field9 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field9")

cassettelabel_field10 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field10")
cassettelabel_field11 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field11")
cassettelabel_field12 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field12")


cassettelabel_field13 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field13")
cassettelabel_field14 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field14")
cassettelabel_field15 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field15")
cassettelabel_field16 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field16")
cassettelabel_field17 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field17")
cassettelabel_field18 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field18")
cassettelabel_field19 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field19")
cassettelabel_field20 = Interface_ComboBoxCST(subframe_4_tab1, "cassettelabel_field20")


slidelabel_field1 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field1")
slidelabel_field2 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field2")
slidelabel_field3 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field3")
slidelabel_field4 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field4")
slidelabel_field5 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field5")
slidelabel_field6 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field6")
slidelabel_field7 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field7")
slidelabel_field8 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field8")
slidelabel_field9 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field9")

slidelabel_field10 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field10")
slidelabel_field11 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field11")
slidelabel_field12 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field12")
slidelabel_field13 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field13")
slidelabel_field14 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field14")
slidelabel_field15 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field15")
slidelabel_field16 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field16")
slidelabel_field17 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field17")
slidelabel_field18 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field18")
slidelabel_field19 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field19")
slidelabel_field20 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field20")
slidelabel_field21 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field21")
slidelabel_field22 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field22")
slidelabel_field23 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field23")
slidelabel_field24 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field24")
slidelabel_field25 = Interface_ComboBoxSDL(subframe_4_tab2, "slidelabel_field25")


# Cassette organisation, line 1
cassettelabel_field1.combo_object_cst("Line 1 : ",0,0,0,1)
cassettelabel_field2.combo_object_cst("Line 1 : ",0,0,0,2)
cassettelabel_field3.combo_object_cst("Line 1 : ",0,0,0,3)
cassettelabel_field4.combo_object_cst("Line 1 : ",0,0,0,4)
cassettelabel_field5.combo_object_cst("Line 1 : ",0,0,0,5)

# Cassette organisation, Line 2
cassettelabel_field6.combo_object_cst("Line 2 : ",1,0,1,1)
cassettelabel_field7.combo_object_cst("Line 2 : ",1,0,1,2)
cassettelabel_field8.combo_object_cst("Line 2 : ",1,0,1,3)
cassettelabel_field9.combo_object_cst("Line 2 : ",1,0,1,4)
cassettelabel_field10.combo_object_cst("Line 2 : ",1,0,1,5)

# Cassette organisation, Line 3
cassettelabel_field11.combo_object_cst("Line 3 : ",2,0,2,1)
cassettelabel_field12.combo_object_cst("Line 3 : ",2,0,2,2)
cassettelabel_field13.combo_object_cst("Line 3 : ",2,0,2,3)
cassettelabel_field14.combo_object_cst("Line 3 : ",2,0,2,4)
cassettelabel_field15.combo_object_cst("Line 3 : ",2,0,2,5)

# Cassette organisation, Line 4
cassettelabel_field16.combo_object_cst("Line 4 : ",3,0,3,1)
cassettelabel_field16.box.configure(state='disabled')
cassettelabel_field17.combo_object_cst("Line 4 : ",3,0,3,2)
cassettelabel_field17.box.configure(state='disabled')
cassettelabel_field18.combo_object_cst("Line 4 : ",3,0,3,3)
cassettelabel_field18.box.configure(state='disabled')
cassettelabel_field19.combo_object_cst("Line 4 : ",3,0,3,4)
cassettelabel_field19.box.configure(state='disabled')
cassettelabel_field20.combo_object_cst("Line 4 : ",3,0,3,5)
cassettelabel_field20.box.configure(state='disabled')
# Cassette organisation, Line 5
cassettelabel_field16.combo_object_cst("Line 5 : ",4,0,4,1)
cassettelabel_field16.box.configure(state='disabled')
cassettelabel_field17.combo_object_cst("Line 5 : ",4,0,4,2)
cassettelabel_field17.box.configure(state='disabled')
cassettelabel_field18.combo_object_cst("Line 5 : ",4,0,4,3)
cassettelabel_field18.box.configure(state='disabled')
cassettelabel_field19.combo_object_cst("Line 5 : ",4,0,4,4)
cassettelabel_field19.box.configure(state='disabled')
cassettelabel_field20.combo_object_cst("Line 5 : ",4,0,4,5)
cassettelabel_field20.box.configure(state='disabled')



# Slide organisation, line 1
slidelabel_field1.combo_object_sdl("Line 1 : ",0,0,0,1)
slidelabel_field2.combo_object_sdl("Line 1 : ",0,0,0,2)
slidelabel_field3.combo_object_sdl("Line 1 : ",0,0,0,3)
slidelabel_field4.combo_object_sdl("Line 1 : ",0,0,0,4)
slidelabel_field5.combo_object_sdl("Line 1 : ",0,0,0,5)
# Slide organisation, line 2
slidelabel_field6.combo_object_sdl("Line 2 : ",1,0,1,1)
slidelabel_field7.combo_object_sdl("Line 2 : ",1,0,1,2)
slidelabel_field8.combo_object_sdl("Line 2 : ",1,0,1,3)
slidelabel_field9.combo_object_sdl("Line 2 : ",1,0,1,4)
slidelabel_field10.combo_object_sdl("Line 2 : ",1,0,1,5)
# Slide organisation, line 3
slidelabel_field11.combo_object_sdl("Line 3 : ",2,0,2,1)
slidelabel_field12.combo_object_sdl("Line 3 : ",2,0,2,2)
slidelabel_field13.combo_object_sdl("Line 3 : ",2,0,2,3)
slidelabel_field14.combo_object_sdl("Line 3 : ",2,0,2,4)
slidelabel_field15.combo_object_sdl("Line 3 : ",2,0,2,5)
# Slide organisation, line 4
slidelabel_field16.combo_object_sdl("Line 4 : ",3,0,3,1)
slidelabel_field17.combo_object_sdl("Line 4 : ",3,0,3,2)
slidelabel_field18.combo_object_sdl("Line 4 : ",3,0,3,3)
slidelabel_field19.combo_object_sdl("Line 4 : ",3,0,3,4)
slidelabel_field20.combo_object_sdl("Line 4 : ",3,0,3,5)
# Slide organisation, line 5
slidelabel_field21.combo_object_sdl("Line 5 : ",4,0,4,1)
slidelabel_field22.combo_object_sdl("Line 5 : ",4,0,4,2)
slidelabel_field23.combo_object_sdl("Line 5 : ",4,0,4,3)
slidelabel_field24.combo_object_sdl("Line 5 : ",4,0,4,4)
slidelabel_field25.combo_object_sdl("Line 5 : ",4,0,4,5)

################################################################################################
################################################################################################
################################################################################################

################################################################################################
################################## WAITING LIST ################################################
################################################################################################

tk.Label(subframe_6, text="Type || Port || Hopper || Nombre || Champs").pack(side=tk.TOP, fill=tk.BOTH)
waitinglist.waitinglist()

################################################################################################
################################################################################################
################################################################################################

################################################################################################
################################## COMMAND BUTTONS #####################################################
################################################################################################

btn_load_profile = tk.Button(subframe_3, text="Charger profil", bg='CadetBlue2', 
 command=Special_Functions.load_profile).pack(side=tk.LEFT, fill=tk.BOTH)

btn_save_profile = tk.Button(subframe_3, text="Sauvegarder profil", bg='CadetBlue3', 
 command=Special_Functions.save_profile).pack(side=tk.RIGHT, fill=tk.BOTH)

btn_send_to_queue = tk.Button(subframe_5, text="Envoyer à la liste d'attente", bg='rosy brown', 
 command=Special_Functions.send_to_queue).grid(row=1, column=0)

btn_send_command = tk.Button(subframe_6, text="Démarrer gravure", bg='indian red', 
 command=Special_Functions.run_sc_thr).pack(side=tk.TOP, fill=tk.BOTH, padx=2, pady=3)

btn_eject_slide = tk.Button(subframe_7, text="Eject. (GLM)", bg='SlateGray2', 
 command=Special_Functions.eject_command_slide).grid(row=0, column=0)

btn_eject_cassette = tk.Button(subframe_7, text="Eject. (GCS)", bg='SlateGray3', 
 command=Special_Functions.eject_command_cassette).grid(row=0, column=1)

btn_reset_cassettewriter = tk.Button(subframe_7, text="Reset (GCS)", bg='ivory2', 
command=Special_Functions.reset_cassettewriter_command).grid(row=0, column=2)

btn_reset_slidewriter = tk.Button(subframe_7, text="Reset (GLM)", bg='ivory3', 
command=Special_Functions.reset_slidewriter_command).grid(row=0, column=3)

btn_stop_after_cassette = tk.Button(subframe_7, text="Stop (GCS)", bg='bisque3', 
 command=Special_Functions.stop_after_cassette_command).grid(row=0, column=4)

btn_stop_after_slide = tk.Button(subframe_7, text="Stop (GLM)", bg='bisque4', 
 command=Special_Functions.stop_after_slide_command).grid(row=0, column=5)

btn_load_slide = tk.Button(subframe_7, text="Charg. (GLM)", bg='AntiqueWhite3', 
 command=Special_Functions.load_slide_command).grid(row=0, column=6)

################################################################################################
################################################################################################
################################################################################################

################################################################################################
###################################### INTERFACE END  ##########################################
################################################################################################

# End of subframe 1
subframe_1.pack(side=tk.TOP)
# End of subframe 2
subframe_2.pack(side=tk.TOP)
## End of Main menu
main_window.config(menu = barre_menu)
# End of subframe 3
subframe_3.pack(side=tk.TOP)
## End of mainframe LEFT
frame_left.pack(side=tk.LEFT)
# End of subframe 4
subframe_4.pack(side=tk.TOP, fill=tk.BOTH, padx=2, pady=3)
# End of subframe 5
subframe_5.pack(side=tk.TOP, fill=tk.BOTH, padx=2, pady=3)
# End of subframe 6
subframe_6.pack(side=tk.TOP, fill=tk.BOTH, padx=2, pady=3)
# End of subframe 7
subframe_7.pack()
## End of mainframe RIGHT
frame_right.pack(side=tk.RIGHT)
### End of the main window loop
main_window.mainloop()

################################################################################################
################################################################################################
################################################################################################
