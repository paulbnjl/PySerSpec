# PySerSpec
Simple python software to control Shimadzu UVmini-1240 spectrophotometer, linked to the computer using a serial RS232 cable.

It allows you to control it while in "PC control mode" (F4), and supports all parameters mentionned in the official documentation :
Gain/light/wavelength/mode/data accumulation time settings, temporal scan, spectrum scan, punctual measurement.
I've also tried to implement functions related to optionnals multi-cells holders and sippers.
But since I don't have access to these, it's totally untested !

Documentation is available here :
https://extranet.fisher.co.uk/webfiles/fr/Pjointes/Mdemploi/SHI001_FR%20SPECTROPHOTOMETRE%201240.pdf (in French ; p96-p109)

In order to use it, it is required to have installed :
  x At least python 3.4 : https://www.python.org/downloads/
  x Pyserial : https://pythonhosted.org/pyserial/
  x Matplotlib : http://matplotlib.org/
  
  To use it, assuming that you installed all the required dependencies, you just have to run the PySerSpec.py file.
  For instance, on GNU/Linux : python3.4 PySerSpec.py
  
  If you perform measurements with it, note that anything send back by the machine is saved in .csv files, under the data/ folder.
  "Corrected" values are values where the negative values (i.e values under what was measured for the blank sample) have been replaced by 0.
  "Raw" values are the ones actually sent by the spectrophotometer.
