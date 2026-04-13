from defragmentation_fuel import defragmenter_carburant
#from verifier_crashes import verifier_crashes  "fonction supprimée et réhabiliter dans le main_Titi et main_final
from tri_insertion.py import insertion_tri_score

def simuler_tour(liste_avions, policy):
    """
    Simule un tour :
    1. Trie les avions selon la policy.
    2. Le premier avion de la liste atterrit (est retiré).
    3. Réduit le carburant des autres avions.
    4. Vérifie les crashes.
    Retourne :
    - avions_atterris : liste des avions ayant atterri
    - avions_crashes : liste des avions crashés
    - avions_en_attente : liste des avions encore en vol
    """
    # Tri selon la policy
    liste_triee, _ = insertion_tri_score(liste_avions.copy(), policy)

    # L'avion avec la plus haute priorité atterrit
    avion_atterri = liste_triee.pop(0)

    # Réduit le carburant des autres
    defragmenter_carburant(liste_triee)

    # Vérifie les crashes
    avions_crashes, avions_en_attente = verifier_crashes(liste_triee)

    return [avion_atterri], avions_crashes, avions_en_attente