import os
import numpy as np
import math
import pickle

def akt_funk(wert):
    return 1 / (1 + math.e ** (-wert))

def erkenne_zahl(pixel_liste):
	pfad_zu_gewichte = os.path.abspath(".")
	datei = open(pfad_zu_gewichte + os.path.sep + "mysite" + os.path.sep + "Gewichte" + os.path.sep + "gew_hid_out.gew", "rb")
	gew_hid_out = pickle.load(datei)
	datei = open(pfad_zu_gewichte + os.path.sep + "mysite" + os.path.sep + "Gewichte" + os.path.sep + "gew_in_hid.gew", "rb")
	gew_in_hid = pickle.load(datei)

	in_neu = []

	# Erzeugen der Hiddenneuronen
	hid_neu_ohne_np = [[1.0]]
	for _ in range(0, 28):
		hid_neu_ohne_np.append([0.0])
	hid_neu = np.array(hid_neu_ohne_np)

	# Erzeugen der Outputneuronen
	out_neu_ohne_np = []
	for i in range(0, 2):
		wert = [0.0]
		out_neu_ohne_np.append(wert)
	out_neu = np.array(out_neu_ohne_np)

	# Erzeugen der Inputneuronen
	in_neu = np.array(pixel_liste)

	# Daten durchlaufen lassen
	net_i_hid = np.dot(gew_in_hid, in_neu)
	for i in range(0, len(net_i_hid)):
		hid_neu[i + 1][0] = akt_funk(net_i_hid[i][0])
	net_i_out = np.dot(gew_hid_out, hid_neu)
	for i in range(0, len(net_i_out)):
		out_neu[i][0] = akt_funk(net_i_out[i][0])

	#print(out_neu)
	#print("Die Zahl ist: "+str(out_neu.argmax()))
	return out_neu.argmax()