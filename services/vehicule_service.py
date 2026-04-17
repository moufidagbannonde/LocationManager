from services.data_manager import charger_donnees, sauvegarder_donnees
from services.display import afficher_vehicule
from models.vehicule import Vehicule
from utils.generator import generate_id

FICHIER_VEHICULES = "data/vehicules.json"


def get_vehicules():
    return charger_donnees(FICHIER_VEHICULES)


def ajouter_vehicule(immatriculation, marque, modele, prix):
    vehicules = get_vehicules()
    immat = immatriculation.strip().upper()
    if any(v["immatriculation"] == immat for v in vehicules):
        print("❌ Immatriculation déjà existante")
        return
    vehicule = Vehicule(generate_id(vehicules), immat, marque, modele, prix)
    vehicules.append(vehicule.to_dict())
    sauvegarder_donnees(FICHIER_VEHICULES, vehicules)
    print(f"✅ Véhicule ajouté — {immat}")


def lister_vehicules():
    vehicules = get_vehicules()
    if not vehicules:
        print("⚠️ Aucun véhicule trouvé")
        return
    for v in vehicules:
        afficher_vehicule(v)


def vehicules_disponibles():
    disponibles = [v for v in get_vehicules() if v["disponible"]]
    if not disponibles:
        print("⚠️ Aucun véhicule disponible")
        return
    for v in disponibles:
        afficher_vehicule(v)


def modifier_vehicule(immatriculation, marque=None, modele=None, prix=None):
    vehicules = get_vehicules()
    immat = immatriculation.strip().upper()
    for v in vehicules:
        if v["immatriculation"] == immat:
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


def supprimer_vehicule(immatriculation):
    vehicules = get_vehicules()
    immat = immatriculation.strip().upper()
    new_vehicules = [v for v in vehicules if v["immatriculation"] != immat]
    if len(new_vehicules) == len(vehicules):
        print("❌ Véhicule non trouvé")
        return
    sauvegarder_donnees(FICHIER_VEHICULES, new_vehicules)
    print("✅ Véhicule supprimé")


def filtrer_par_prix(prix_max):
    result = [v for v in get_vehicules() if v["prix_par_jour"] <= prix_max]
    if not result:
        print("⚠️ Aucun véhicule dans cette gamme de prix")
        return
    for v in result:
        afficher_vehicule(v)


def set_disponibilite(immatriculation, disponible):
    vehicules = get_vehicules()
    for v in vehicules:
        if v["immatriculation"] == immatriculation:
            v["disponible"] = disponible
            sauvegarder_donnees(FICHIER_VEHICULES, vehicules)
            return True
    return False


def get_vehicule_par_immat(immatriculation):
    immat = immatriculation.strip().upper()
    return next((v for v in get_vehicules() if v["immatriculation"] == immat), None)
