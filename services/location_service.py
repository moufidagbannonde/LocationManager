from services.data_manager import charger_donnees, sauvegarder_donnees
import services.vehicule_service as vs
import services.client_service as cs
from utils.generator import generate_id
from datetime import datetime, timedelta

FICHIER_LOCATIONS = "data/locations.json"


def get_locations():
    return charger_donnees(FICHIER_LOCATIONS)


def louer_vehicule(client_id, immatriculation, jours):
    clients = cs.get_clients()
    if not any(c["id"] == client_id for c in clients):
        return None, "Client introuvable"

    vehicule = vs.get_vehicule_par_immat(immatriculation)
    if vehicule is None:
        return None, "Véhicule introuvable"
    if not vehicule["disponible"]:
        return None, "Véhicule indisponible"

    date_debut = datetime.now()
    date_fin = date_debut + timedelta(days=jours)

    locations = get_locations()
    location = {
        "id": generate_id(locations),
        "immatriculation": vehicule["immatriculation"],
        "client_id": client_id,
        "jours": jours,
        "date_debut": date_debut.strftime("%Y-%m-%d"),
        "date_fin": date_fin.strftime("%Y-%m-%d"),
        "statut": "en_cours"
    }
    locations.append(location)
    sauvegarder_donnees(FICHIER_LOCATIONS, locations)
    vs.set_disponibilite(vehicule["immatriculation"], False)
    return location, None


def retourner_vehicule(location_id):
    locations = get_locations()
    loc = next((l for l in locations if l["id"] == location_id), None)
    if loc is None:
        return False, "Location introuvable"
    if loc["statut"] == "terminee":
        return False, "Location déjà terminée"
    vs.set_disponibilite(loc["immatriculation"], True)
    loc["statut"] = "terminee"
    sauvegarder_donnees(FICHIER_LOCATIONS, locations)
    return True, None


def voir_locations():
    return [l for l in get_locations() if l["statut"] == "en_cours"]


def locations_par_client(client_id):
    return [l for l in get_locations() if l["client_id"] == client_id]


def locations_en_cours_par_client(client_id):
    return [l for l in get_locations() if l["client_id"] == client_id and l["statut"] == "en_cours"]


def top_vehicules():
    compteur = {}
    for loc in get_locations():
        immat = loc["immatriculation"]
        compteur[immat] = compteur.get(immat, 0) + 1
    return sorted(compteur.items(), key=lambda x: x[1], reverse=True)


def calcul_prix(immatriculation, jours):
    vehicule = vs.get_vehicule_par_immat(immatriculation)
    if vehicule:
        return vehicule["prix_par_jour"] * jours
    return 0


def total_gains():
    return sum(calcul_prix(loc["immatriculation"], loc["jours"]) for loc in get_locations())
