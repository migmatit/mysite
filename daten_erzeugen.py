import os, sys
import traceback
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')


import django
django.setup()

from marcador.models import Vokabel
try:
	pfad_zu_vokabeln = os.path.abspath(".")
	anzahl_kapitel = 0
	for kapitel in os.listdir(pfad_zu_vokabeln):
		anzahl_kapitel = anzahl_kapitel + 1
		pfad_zum_kapitel = pfad_zu_vokabeln + os.path.sep + "Kapitel" + os.path.sep +"norsk_kap_" + str(anzahl_kapitel) + ".txt"
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
	input()
except Exception as e:
	print(traceback.format_exception(None, # <- type(e) by docs, but ignored 
                                     e, e.__traceback__),
          file=sys.stderr, flush=True)
	input()
