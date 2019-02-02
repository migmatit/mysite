import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')


import django
django.setup()

from marcador.models import Vokabel

pfad_zu_vokabeln = \
		"C:/Users/Bernd Holter/Documents/python/projekte/uebungen/vokabeltrainer/vokabeln/"
anzahl_kapitel = 0
for kapitel in os.listdir(pfad_zu_vokabeln):
	anzahl_kapitel = anzahl_kapitel + 1
	pfad_zum_kapitel = pfad_zu_vokabeln + "norsk_kap_" + str(anzahl_kapitel) + ".txt"
	vokabeln = open(pfad_zum_kapitel)
	for line in vokabeln:
		line = line.strip(" ")
		line = line.rstrip()
		aufteilen = line.split(":")
		norw = aufteilen[0]
		deu = aufteilen[1]
		print(aufteilen)
		v = Vokabel(norwegisch=norw, deutsch=deu, kapitel=anzahl_kapitel)
		v.save()
		
	vokabeln.close()