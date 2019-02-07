from django.shortcuts import render
from django.db.models import Max
from .models import Vokabel
import random

# Create your views here.

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