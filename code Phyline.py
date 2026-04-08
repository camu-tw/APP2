def extraction_avions (liste_avions):
    groupe_medical = []
    groupe_technique = []
    groupe_standard = []
    fuel_trié = [] 
    for avion in liste_avions:
        if avion['medical'] == True:
            groupe_medical.append(avion)
        elif avion['technical_issue'] == True:
            groupe_technique.append(avion)
        else:
            groupe_standard.append(avion)
    for groupe in [groupe_medical, groupe_technique, groupe_standard]:
        for i in range(1, len(groupe)):
            avion_actuel = groupe[i]
            j = i - 1
            while j >= 0 and groupe[j]['fuel'] > avion_actuel['fuel']:
                groupe[j + 1] = groupe[j]
                j -= 1
            groupe[j + 1] = avion_actuel

    fuel_trié = groupe_medical + groupe_technique + groupe_standard
    
    return fuel_trié