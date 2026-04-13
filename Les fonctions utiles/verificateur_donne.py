#Fonction coherance de donné, on verifie si toutes les clées on bien ete entrée

import données.APP_datasets as APP_datasets

listes_avion = APP_datasets.avions

def verification_donne(listes_avion):
    erreurs = []
    # On parcourt la liste de dictionnaires et on verifie cles + valeurs.
    if not listes_avion:
        erreurs.append({"erreur n°": "global", "erreur": "La liste des avions est vide"})
        return erreurs

    for elst,edico in enumerate(listes_avion):
        # Verification de la cle id + validation souple du nom d'avion.
        if "id" not in edico:
            erreurs.append({"erreur n°":edico,"erreur": "La clé id est manquante"})
        else:
            id_avion = edico.get("id")
            if not isinstance(id_avion, str):
                erreurs.append({"erreur n°":edico,"erreur": "La valeur de id doit etre une chaine"})
            else:
                id_avion = id_avion.strip()
                if len(id_avion) < 2 or len(id_avion) > 40:
                    erreurs.append({"erreur n°":edico,"erreur": "La valeur de id est trop courte ou trop longue"})
                # c.isalnum() est True si c est une lettre ou un chiffre.
                # Ici, on colle au dataset: id doit etre uniquement alphanumerique (pas d'espace, -, _, etc.).
                elif not all(c.isalnum() for c in id_avion):
                    erreurs.append({"erreur n°":edico,"erreur": "La valeur de id contient des caracteres invalides"})
                elif not any(c.isalpha() for c in id_avion):
                    erreurs.append({"erreur n°":edico,"erreur": "La valeur de id doit contenir au moins une lettre"})

        # Verification de la cle fuel et du type/borne.
        if "fuel" not in edico:
            erreurs.append({"erreur n°":edico,"erreurs": "La clé fuel est manquante"})
        else:
            if not isinstance(edico.get("fuel"), (int, float)):
                erreurs.append({"erreur n°":edico,"erreur": "La valeur de fuel doit etre un nombre"})
            elif edico.get("fuel") < 0:
                erreurs.append({"erreur n°":edico,"erreur": "La valeur de fuel doit etre positive"})

        # Verification de la cle medical.
        if "medical"not in edico:
            erreurs.append({"erreur n°":edico,"erreur": "La clé medical est manquante"})
        else:
            if not isinstance(edico.get("medical"), bool):
                erreurs.append({"erreur n°":edico,"erreur": "La valeur de medical doit etre un booleen"})

        # Verification de la cle technical_issue.
        if "technical_issue" not in edico:
            erreurs.append({"erreur n°":edico,"erreur": "La clé technical_issue est manquante"})
        else:
            if not isinstance(edico.get("technical_issue"), bool):
                erreurs.append({"erreur n°":edico,"erreur": "La valeur de technical_issue doit etre un booleen"})

        # Verification de la cle diplomatic_level.
        if "diplomatic_level" not in edico:
            erreurs.append({"erreur n°":edico,"erreur": "La clé technical_issue est manquante"})
        else:
            if not isinstance(edico.get("diplomatic_level"), int):
                erreurs.append({"erreur n°":edico,"erreur": "La valeur de diplomatic_level doit etre un entier"})
            elif edico.get("diplomatic_level") < 0 or edico.get("diplomatic_level") > 5:
                erreurs.append({"erreur n°":edico,"erreur": "La valeur de diplomatic_level doit etre entre 0 et 5"})

    # Retour de toutes les erreurs detectees (liste vide si tout est correct).
    return erreurs



