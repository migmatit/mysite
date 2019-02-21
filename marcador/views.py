from django.shortcuts import render
from django.db.models import Max
from .models import Vokabel
import random
import json

# Create your views here.

def index(request):
	
	return render(request, 'index.html', {})

def eingang(request):
	#Zum Testen muß die Session-DB gelöscht werden!!!
	request.session.flush()
	kapitel_dict = Vokabel.objects.all().aggregate(Max('kapitel'))
	anzahl_kapitel = kapitel_dict['kapitel__max']
	kapitelnummern = []
	abschlussmeldung = ""
	for i in range(1, anzahl_kapitel + 2):
		if i < anzahl_kapitel + 1:
			kapitelnummern.append(str(i))
		else:
			kapitelnummern.append("alles")
		
	if request.POST.get('ende') == 'ja':
		abschlussmeldung = 'Sie hatten ' + str(request.POST['richtige_antworten']) + ' von ' + str(request.POST['alle']) + ' richtig.'
	#im Pfad zu 'hallo.html' muss nicht der templates-Ordner
	#angegeben werden; ist automatisch in settings verarbeitet
	return render(request, 'eingang.html', {'kapitelnummern': kapitelnummern, \
											'abschlussmeldung': abschlussmeldung})

def vokabeltest(request):
	auswahl = {}
	
	if 'restvokabeln' in request.session:
		auswahl = request.session['restvokabeln']
		request.session['richtige_antworten'] = request.POST['richtige_antworten']
	
	else:
		if 'Kapitel alles' in request.POST:
			alles = Vokabel.objects.all()
			for zeile in alles:
				if request.POST['uebersetzung'] == 'norw_deu':
					auswahl[zeile.norwegisch] = zeile.deutsch
					request.session['uebersetzung'] = 'norw_deu'
				else:
					auswahl[zeile.deutsch] = zeile.norwegisch
					request.session['uebersetzung'] = 'deu_norw'
		else:
			for line in request.POST:
				if 'Kapitel' in line:
					aufteilen = line.split(" ")
					ein_kapitel = Vokabel.objects.filter(kapitel=aufteilen[1])
					for zeile in ein_kapitel:
						if request.POST['uebersetzung'] == 'norw_deu':
							auswahl[zeile.norwegisch] = zeile.deutsch
							request.session['uebersetzung'] = 'norw_deu'
						else:
							auswahl[zeile.deutsch] = zeile.norwegisch
							request.session['uebersetzung'] = 'deu_norw'
		request.session['anzahl_der_ausgangsvokabeln'] = len(auswahl)
		request.session['richtige_antworten'] = 0
	
	# if request.session['uebersetzung'] == 'deu_norw':
		# uebersetzung = 'deu_norw'
	anzahl_der_ausgangsvokabeln = request.session['anzahl_der_ausgangsvokabeln']
	wort1, wort2 = random.choice(list(auswahl.items()))
	del auswahl[wort1]
	anzahl_vokabeln = len(auswahl)
	request.session['restvokabeln'] = auswahl
	
	return render(request, 'vokabeltest.html', {'wort1':wort1, \
												'wort2':wort2, \
												'anzahl_vokabeln':anzahl_vokabeln, \
												'anzahl_der_ausgangsvokabeln':anzahl_der_ausgangsvokabeln, \
												'richtige_antworten':request.session['richtige_antworten'],
												'uebersetzung':request.session['uebersetzung']})

def sudoku(request):
	rueckgabe = []
	fehler = True
	fehlermeldung = "Geben Sie Zahlen (1-9) ein, damit es ein Sudoku werden kann."
	button_belegung = "Sudoku abschicken"
	belegte_felder = []

	if 'feld_1' in request.POST:
		if request.POST['hidden1'] == 'Sudoku abschicken':
			import sudoku.sudoku as sudoku
			d = {}
			die_gruppen = []
			felder_mit_wert = {}
			zaehler = 1
			
			for i in range(1, 82):		
				if zaehler > 9:
					zaehler = 1
				zeile = (i // 10) + 1
				spalte = zaehler
				wert = request.POST['feld_' + str(i)]
				if wert != '':
					felder_mit_wert[(zeile, spalte)] = int(wert)
					
					belegte_felder.append((zeile - 1) * 9 + spalte)
				print(zeile, i, zeile, spalte)
				zaehler = zaehler + 1
			
			sudoku.erzeuge_ort_wert(1, 9, d)
			sudoku.belege_sudoku_mit_werten(d, felder_mit_wert)
			sudoku.erzeuge_gruppen(1, 9, die_gruppen)
			
			if sudoku.zulaessige_zahlen(d, die_gruppen):
				sudoku.loese_sudoku([0], d.copy(), die_gruppen, rueckgabe)
				button_belegung = 'Nächstes Sudoku'
				fehlermeldung = ""
			else:
				fehlermeldung = 'Sie haben zwei gleiche Zahlen in einer Reihe, Zeile oder Quadranten gesetzt!'
				belegte_felder = []
			#Kommt nochmal der request von der gelösten Webseite mit den Werten
			#wird in sudoku.py loese_sudoku() [0] auf [1] gesetzt, da ja gelöst.
			#rueckgabe ist dann eine leere Liste, also ist bei der for-Schleife
			#len() gleich Null und die Anfangsseite vom Sudokufeld wird gezeigt.
	sudokufeld = []
	for i in range(1, 82):
		#Tupel werden erzeugt; sind leichter mit Django-Tag auszulesen 
		#(.-Operator: feldnr.0)
		if len(rueckgabe) > 0:
			sudokufeld.append((i, rueckgabe[i - 1]))
		else:
			sudokufeld.append((i, ''))
	
	return render(request, 'sudoku.html', {'sudokufeld': sudokufeld, 
											'fehlermeldung': fehlermeldung, 
											'button_belegung': button_belegung,
											'belegte_felder': belegte_felder})