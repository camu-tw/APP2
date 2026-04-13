


def trouver_minimum(lst):
	# Verifie que la liste n'est pas vide.
	if len(lst) == 0:
		raise ValueError("La liste ne peut pas etre vide.")

	# On suppose que le premier element est le minimum au depart.
	minimum = lst[0]

	# On parcourt toute la liste pour trouver une valeur plus petite.
	for nombre in lst:
		if nombre < minimum:
			minimum = nombre

	# On retourne le plus petit nombre trouve.
	return minimum

