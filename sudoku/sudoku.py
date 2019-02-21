def erzeuge_ort_wert(ZAHL_MIN, ZAHL_MAX, d):
	for i in range(ZAHL_MIN, ZAHL_MAX + 1):
		for j in range(ZAHL_MIN, ZAHL_MAX + 1):
			t = i, j
			d[t] = 0
	return d

def belege_sudoku_mit_werten(d, wertbelegung):
	wertbelegung_keys = wertbelegung.keys()
	for key in wertbelegung_keys:
		d[key] = wertbelegung[key]

def erzeuge_gruppen(ZAHL_MIN, ZAHL_MAX, die_gruppen):
	gruppe_1 = []
	gruppe_2 = []
	gruppe_3 = []
	gruppe_4 = []
	gruppe_5 = []
	gruppe_6 = []
	gruppe_7 = []
	gruppe_8 = []
	gruppe_9 = []
	
	for i in range(ZAHL_MIN, ZAHL_MAX + 1):
		for j in range(ZAHL_MIN, ZAHL_MAX + 1):
			if i <= 3 and j <= 3:
				gruppe_1.append((i, j))
			if i <= 3 and j >= 4 and j <= 6:
				gruppe_2.append((i, j))
			if i <= 3 and j >= 7:
				gruppe_3.append((i, j))
			if i >= 4 and i <= 6 and j <= 3:
				gruppe_4.append((i, j))
			if i >= 4 and i <= 6 and j >= 4 and j <= 6:
				gruppe_5.append((i, j))
			if i >= 4 and i <= 6 and j >= 7:
				gruppe_6.append((i, j))
			if i >= 7 and j <= 3:
				gruppe_7.append((i, j))
			if i >= 7 and j >= 4 and j <= 6:
				gruppe_8.append((i, j))
			if i >= 7 and j >= 7:
				gruppe_9.append((i, j))
	
	die_gruppen.append(gruppe_1)
	die_gruppen.append(gruppe_2)
	die_gruppen.append(gruppe_3)
	die_gruppen.append(gruppe_4)
	die_gruppen.append(gruppe_5)
	die_gruppen.append(gruppe_6)
	die_gruppen.append(gruppe_7)
	die_gruppen.append(gruppe_8)
	die_gruppen.append(gruppe_9)

def gib_erstes_freies_feld(tabelle):
	for feld in tabelle:
		if tabelle[feld] == 0:
			return feld

def gib_tabelle_aus(ZAHL_MIN, ZAHL_MAX, tabelle):
	for i in range(ZAHL_MIN, ZAHL_MAX + 1):
		for j in range(ZAHL_MIN, ZAHL_MAX + 1):
			t = i, j
			if j < ZAHL_MAX:
				print(str(tabelle[t]), end = " ")
			else:
				print(str(tabelle[t]))

def gib_zahlen_meiner_gruppen(ZAHL_MIN, ZAHL_MAX, feldtupel, tabelle, die_gruppen):
	zahlen_der_gruppen = []
	zeile = feldtupel[0]
	spalte = feldtupel[1]
	spalte_links = spalte -1
	spalte_rechts = spalte + 1
	zeile_oben = zeile - 1
	zeile_unten = zeile + 1
	
	#horizontale_gruppe bearbeiten
	#erst nach links
	while spalte_links > ZAHL_MIN - 1:
		zahl = tabelle[zeile, spalte_links]
		if zahl > 0:
			zahlen_der_gruppen.append(zahl)
		spalte_links = spalte_links - 1
	#nach rechts
	while spalte_rechts < ZAHL_MAX + 1:
		zahl = tabelle[zeile, spalte_rechts]
		if zahl > 0:
			zahlen_der_gruppen.append(zahl)
		spalte_rechts = spalte_rechts + 1
	
	#vertikale_gruppe
	#erst nach oben
	while zeile_oben > ZAHL_MIN - 1:
		zahl = tabelle[zeile_oben, spalte]
		if zahl > 0:
			zahlen_der_gruppen.append(zahl)
		zeile_oben = zeile_oben - 1
	#nach unten
	while zeile_unten < ZAHL_MAX + 1:
		zahl = tabelle[zeile_unten, spalte]
		if zahl > 0:
			zahlen_der_gruppen.append(zahl)
		zeile_unten = zeile_unten + 1
	
	#Kontrolle, welche Gruppe dazugehört
	for gruppe in die_gruppen:
		if feldtupel in gruppe:
			for feld in gruppe:
				if feldtupel != feld and tabelle[feld] != 0:
					zahlen_der_gruppen.append(tabelle[feld])
			break
	
	return zahlen_der_gruppen

def zulaessige_zahlen(tabelle, die_gruppen):
	ok = True
	for ein_tupel in tabelle:
		wert = tabelle[ein_tupel]
		zahlen_der_gruppen = gib_zahlen_meiner_gruppen(1, 9, ein_tupel, tabelle, die_gruppen)
		if wert in set(zahlen_der_gruppen):
			ok = False
			break

	return ok

def ist_sudoku_geloest(sudoku):
	geloest = True
	for feld in sudoku:
		if sudoku[feld] == 0:
			geloest = False
			break
	return geloest

def loese_sudoku(geloest, tabelle, die_gruppen, rueckgabe):
	#Sonst gibt er die moeglichen sudokus aus, das dauert!
	if geloest[0] != 1:
		moegliche_werte = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		freies_feld = gib_erstes_freies_feld(tabelle)
		#Schnittmenge bilden
		freie_werte = set(moegliche_werte) - set(gib_zahlen_meiner_gruppen(1, 9, freies_feld, tabelle, die_gruppen))
		ein_freier_wert = 0
		
		for wert in freie_werte:
			tabelle[freies_feld] = wert
			if ist_sudoku_geloest(tabelle):
				# gib_tabelle_aus(1, 9, tabelle)
				geloest[0] = 1
				for schluessel in tabelle:
					rueckgabe.append(tabelle[schluessel])
				return rueckgabe

			else:
				loese_sudoku(geloest, tabelle.copy(), die_gruppen, rueckgabe)