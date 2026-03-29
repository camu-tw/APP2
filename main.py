"""
Module principal - Simulation d'atterrissage d'avions en crise
Aéroport de Roissy - 19h42
"""

# Imports des modules du projet
import APP_datasets  # Pour les données des avions
from policies import policy_fuel, policy_medical, policy_diplomatic  # Les différentes règles de priorité
from tris import tri_insertion, tri_selection  # Les algorithmes de tri
from simulation import simuler_atterrissages, afficher_bilan  # La simulation
from verificateur_donne import verification_donne  # Vérifier que les données sont correctes
from generate_random_traffic import generate_random_traffic  # Générer des avions au hasard
import time  # Pour mesurer le temps


def main():
    """
    Fonction principale du programme.
    Elle contrôle le flux du programme et permet à l'utilisateur
    de choisir un scénario et une politique d'atterrissage.
    """
    
    # Bienvenue
    print("="*70)
    print("SIMULATION ATTERRISSAGE - AÉROPORT DE ROISSY (Tempête Exceptionnelle)")
    print("="*70)
    print("\n⚠️  SITUATION CRITIQUE: 19h42")
    print("   - 2 pistes fermées")
    print("   - 1 seule piste opérationnelle")
    print("   - Multiple avions en approche")
    print()
    
    # Charger les données initiales
    print("📥 Chargement des données...")
    avions = APP_datasets.AVIONS_INITIAL  # On utilise le dataset avec 24 avions
    print(f"   ✓ {len(avions)} avions chargés")
    
    # Vérifier que les données sont correctes
    print("\n🔍 Vérification de la cohérence des données...")
    erreurs = verification_donne(avions)
    
    if erreurs:
        # S'il y a des erreurs, les afficher et arrêter
        print(f"   ❌ {len(erreurs)} erreur(s) détectée(s) !")
        for erreur in erreurs:
            print(f"      - {erreur}")
        return
    else:
        # Si pas d'erreur, continue
        print("   ✓ Toutes les données sont valides")
    
    # Afficher le premier avion comme exemple
    print("\n📋 Exemple d'avion dans le dataset:")
    premier_avion = avions[0]
    print(f"   ID: {premier_avion['id']}")
    print(f"   Carburant restant: {premier_avion['fuel']} minutes")
    print(f"   Urgence médicale: {premier_avion['medical']}")
    print(f"   Incident technique: {premier_avion['technical_issue']}")
    print(f"   Importance diplomatique: {premier_avion['diplomatic_level']} / 5")
    print(f"   Heure d'arrivée prévue: {premier_avion['arrival_time']}")
    
    # Copier la liste (pour ne pas modifier l'original)
    avions_a_trier = [avion.copy() for avion in avions]
    
    # Utiliser le tri par insertion avec la politique carburant minimal
    print("\n▶ Tri des avions en cours...")
    print("   Algorithme: Tri par insertion")
    print("   Politique: Priorité carburant minimal")
    
    # Mesurer le temps d'exécution
    temps_debut = time.time()
    
    # Appeler la fonction de tri (elle sera complétée plus tard)
    # ordre_atterrissage, stats = tri_insertion(avions_a_trier, policy_fuel)
    
    # Pour l'instant, on va juste afficher qu'on attend la fonction
    print("   ⏳ En attente de l'implémentation de tri_insertion...")
    
    temps_fin = time.time()
    # temps_execution = temps_fin - temps_debut
    
    # Afficher les résultats du tri (à faire quand tri_insertion sera prête)
    # print(f"\n✓ Tri complété en {temps_execution:.4f} secondes")
    # print(f"  Nombre de comparaisons: {stats['comparisons']}")
    
    # Afficher les top 5 avions prioritaires
    # print(f"\n🛬 Ordre d'atterrissage (5 premiers) :")
    # for i, avion in enumerate(ordre_atterrissage[:5], 1):
    #     print(f"   {i}. {avion['id']} (Fuel: {avion['fuel']}min)")
    
    # Simulation dynamique de l'atterrissage (à faire plus tard)
    # print("\n▶ Simulation de l'atterrissage...")
    # avions_sauves, avions_crashs = simuler_atterrissages(ordre_atterrissage)
    # afficher_bilan(avions_sauves, avions_crashs, stats, temps_execution)
    
    print("\n" + "="*70)
    print("FIN DE LA SIMULATION")
    print("="*70)


# Point d'entrée du programme
if __name__ == "__main__":
    main()
