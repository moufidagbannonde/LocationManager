import json
import os

def charger_donnees(fichier):
    if not os.path.exists(fichier):
        return []
    
    with open(fichier, "r") as f:
        try:
            return json.load(f)
        except:
            return []

def sauvegarder_donnees(fichier, data):
    with open(fichier, "w") as f:
        json.dump(data, f, indent=4)