def defragmenter_carburant(liste_avions, minutes_ecoulees=5):
    """
    Réduit le carburant de chaque avion de 1 fuel toutes les 5 minutes.
    Retourne la liste mise à jour à chaque tour.
    """
    for avion in liste_avions:
        avion["fuel"] -= minutes_ecoulees // 5  # 1 fuel toutes les 5 minutes
        if avion["fuel"] < 0:
            avion["fuel"] = 0  # Évite les valeurs négatives
    return liste_avions

