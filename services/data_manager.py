import json
import os

def charger_donnees(fichier):
    """
    🔹 Cette fonction lit un fichier JSON et retourne son contenu.

    PARAMÈTRE :
    fichier = chemin du fichier (ex: data/vehicules.json)

    🔥 CAS IMPORTANT :
    - Si le fichier n'existe pas → retourne []
    - Si le fichier est vide ou cassé → retourne []

    """

    # Vérifie si le fichier existe
    if not os.path.exists(fichier):
        return []

    # Ouvre le fichier en mode lecture
    with open(fichier, "r") as f:
        try:
            # Convertit JSON → Python (liste de dictionnaires)
            return json.load(f)        
        except json.JSONDecodeError:
            return []


def sauvegarder_donnees(fichier, data):
    """
    🔹 Cette fonction sauvegarde des données dans un fichier JSON

    PARAMÈTRES :
    fichier = chemin du fichier
    data = liste de dictionnaires

    👉 Exemple :
    [
        {"id": 1, "marque": "Toyota"},
        {"id": 2, "marque": "BMW"}
    ]
    """

    with open(fichier, "w") as f:
        # indent=4 → rend le JSON lisible 
        json.dump(data, f, indent=4)