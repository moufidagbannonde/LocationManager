from services.data_manager import charger_donnees, sauvegarder_donnees
from services.display import afficher_vehicule
from models.vehicule import Vehicule
from utils.generator import generate_id

FICHIER_VEHICULES = "data/vehicules.json"


def get_vehicules():
    return charger_donnees(FICHIER_VEHICULES)





# 🔹 Ajouter véhicule
def ajouter_vehicule(marque, modele, prix):
    vehicules = get_vehicules()
    vehicule = Vehicule(generate_id(vehicules), marque, modele, prix)
    vehicules.append(vehicule.to_dict())
    sauvegarder_donnees(FICHIER_VEHICULES, vehicules)
    print("✅ Véhicule ajouté avec succès !")


# 🔹 Lister tous les véhicules
def lister_vehicules():
    vehicules = get_vehicules()
    if not vehicules:
        print("⚠️ Aucun véhicule trouvé")
        return
    for v in vehicules:
        afficher_vehicule(v)


# 🔹 Véhicules disponibles
def vehicules_disponibles():
    vehicules = get_vehicules()
    disponibles = [v for v in vehicules if v["disponible"]]
    if not disponibles:
        print("⚠️ Aucun véhicule disponible")
        return
    for v in disponibles:
        afficher_vehicule(v)


# 🔹 Modifier véhicule
def modifier_vehicule(vehicule_id, marque=None, modele=None, prix=None):
    vehicules = get_vehicules()
    for v in vehicules:
        if v["id"] == vehicule_id:
            if marque:
                v["marque"] = marque
            if modele:
                v["modele"] = modele
            if prix:
                v["prix_par_jour"] = prix
            sauvegarder_donnees(FICHIER_VEHICULES, vehicules)
            print("✅ Véhicule modifié")
            return
    print("❌ Véhicule non trouvé")


# 🔹 Supprimer véhicule
def supprimer_vehicule(vehicule_id):
    vehicules = get_vehicules()
    new_vehicules = [v for v in vehicules if v["id"] != vehicule_id]
    if len(new_vehicules) == len(vehicules):
        print("❌ Véhicule non trouvé")
        return
    sauvegarder_donnees(FICHIER_VEHICULES, new_vehicules)
    print("✅ Véhicule supprimé")


# 🔹 Filtrer par prix
def filtrer_par_prix(prix_max):
    vehicules = get_vehicules()
    result = [v for v in vehicules if v["prix_par_jour"] <= prix_max]
    if not result:
        print("⚠️ Aucun véhicule dans cette gamme de prix")
        return
    for v in result:
        afficher_vehicule(v)


# 🔹 Marquer indisponible / disponible (appelé par location_service)
def set_disponibilite(vehicule_id, disponible):
    vehicules = get_vehicules()
    for v in vehicules:
        if v["id"] == vehicule_id:
            v["disponible"] = disponible
            sauvegarder_donnees(FICHIER_VEHICULES, vehicules)
            return True
    return False
