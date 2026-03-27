def extraire_temps_vol_par_carburant(liste_avions):
	#Retourne une liste de dicts avec l'id et le temps de vol restant (en minutes)."""
	return [
		{"id": avion["id"], "temps_vol": avion["fuel"] * 3}
		for avion in liste_avions
	]


def _heure_vers_minutes(heure):
	"""Convertit HH:MM ou HH.MM en minutes."""
	if isinstance(heure, str):
		heure = heure.strip()
		if ":" in heure:
			h, m = heure.split(":", 1)
			return int(h) * 60 + int(m)
		heure = float(heure)

	h = int(heure)
	m = int(round((float(heure) - h) * 100))
	return h * 60 + m


def _minutes_vers_heure(total_minutes):
	"""Convertit des minutes en format HH:MM."""
	h = total_minutes // 60
	m = total_minutes % 60
	return f"{h:02d}:{m:02d}"


def calculer_marge_carburant(liste_avions, espacement_atterrissage_min=2):
	"""Calcule la marge carburant en tenant compte de la file d'atterrissage.

	Champs attendus pour chaque avion:
	- id
	- fuel
	- arrival_time (HH:MM ou HH.MM)
	- temps_vers_aeroport_min (optionnel, defaut 0)
	- conso_par_3min (optionnel, defaut 1)
	"""
	resultat = []
	dernier_atterrissage = None

	for avion in liste_avions:
		arrivee_theorique = _heure_vers_minutes(avion["arrival_time"])
		temps_vers_aeroport = int(avion.get("temps_vers_aeroport_min", 0))
		arrivee_aeroport = arrivee_theorique + temps_vers_aeroport

		if dernier_atterrissage is None:
			atterrissage_prevu = arrivee_aeroport
		else:
			atterrissage_prevu = max(
				arrivee_aeroport,
				dernier_atterrissage + espacement_atterrissage_min,
			)

		conso_par_3min = float(avion.get("conso_par_3min", 1))
		temps_carburant_restant = int((avion["fuel"] * 3) / conso_par_3min)
		heure_limite_carburant = arrivee_theorique + temps_carburant_restant
		marge_minutes = heure_limite_carburant - atterrissage_prevu

		resultat.append(
			{
				"id": avion["id"],
				"arrivee_theorique": _minutes_vers_heure(arrivee_theorique),
				"arrivee_aeroport": _minutes_vers_heure(arrivee_aeroport),
				"atterrissage_prevu": _minutes_vers_heure(atterrissage_prevu),
				"heure_limite_carburant": _minutes_vers_heure(heure_limite_carburant),
				"marge_minutes": marge_minutes,
			}
		)

		dernier_atterrissage = atterrissage_prevu

	return resultat

"""
On peut ce poser aussi la question de la vitesse de l'avion,pck on peut interpreter
de deux maniere, sois les avions on une vitesse indefinie, il peuvent ce depasser
sans que cela n'influe leur consomation du carburant, donc on peut metre des avions
en stande by sans que l'aavion prioritaitr mette 30mn a arriver, sinon cela ne sert 
a rien de mettre des avions prioritaire.
"""



