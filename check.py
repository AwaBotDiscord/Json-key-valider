import json
import sys
import os

def charger_json(fichier):
    """Charge un fichier JSON et renvoie son contenu."""
    if os.path.exists(fichier):
        with open(fichier, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"Le fichier {fichier} n'existe pas.")
        sys.exit(1)

def obtenir_cles_recursive(dictionnaire, chemin_actuel=""):
    """Récupère toutes les clés dans un dictionnaire JSON récursivement avec leur chemin."""
    cles = []
    for cle, valeur in dictionnaire.items():
        nouveau_chemin = f"{chemin_actuel}.{cle}" if chemin_actuel else cle
        if isinstance(valeur, dict):
            cles.extend(obtenir_cles_recursive(valeur, nouveau_chemin))
        else:
            cles.append(nouveau_chemin)
    return cles

def comparer_cles(json1, json2):
    """Compare les clés de deux dictionnaires JSON et renvoie les différences avec les chemins."""
    cles_json1 = set(obtenir_cles_recursive(json1))
    cles_json2 = set(obtenir_cles_recursive(json2))

    # Clés manquantes dans chaque fichier
    cles_manquantes_json1 = cles_json2 - cles_json1
    cles_manquantes_json2 = cles_json1 - cles_json2

    return cles_manquantes_json1, cles_manquantes_json2

def afficher_resultats(cles_manquantes_json1, cles_manquantes_json2):
    """Affiche les clés manquantes avec le chemin d'accès et retourne un code de sortie approprié."""
    if not cles_manquantes_json1 and not cles_manquantes_json2:
        print("Tout est terminé ! 🎊🟢")
        sys.exit(0)
    else:
        print("Résultats de la comparaison des clés :")
        if cles_manquantes_json1:
            print("\n**Clés manquantes dans le second fichier :**")
            for cle in cles_manquantes_json1:
                segments = cle.split('.')
                print(f"- ❌ La clé '{segments[-1]}' est manquante dans {segments[:-1]}")
        
        if cles_manquantes_json2:
            print("\n**Clés manquantes dans le premier fichier :**")
            for cle in cles_manquantes_json2:
                segments = cle.split('.')
                print(f"- ❌ La clé '{segments[-1]}' est manquante dans {segments[:-1]}")
        
        sys.exit(1)

if __name__ == "__main__":
    # Charger les fichiers JSON
    fichier1 = sys.argv[1]
    fichier2 = sys.argv[2]

    json1 = charger_json(fichier1)
    json2 = charger_json(fichier2)

    # Comparer les clés
    cles_manquantes_json1, cles_manquantes_json2 = comparer_cles(json1, json2)

    # Afficher les résultats
    afficher_resultats(cles_manquantes_json1, cles_manquantes_json2)