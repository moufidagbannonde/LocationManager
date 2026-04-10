from services.data_manager import charger_donnees, sauvegarder_donnees
from services.display import afficher_location
import services.vehicule_service as vs
import services.client_service as cs

FICHIER_LOCATIONS = "data/locations.json"


def get_locations():
    return charger_donnees(FICHIER_LOCATIONS)


def generate_id(data):
    if not data:
        return 1
    return max(item["id"] for item in data) + 1


# 🔹 Louer un véhicule
def louer_vehicule(client_id, vehicule_id, jours):
    # Vérifier que le client existe
    clients = cs.get_clients()
    if not any(c["id"] == client_id for c in clients):
        return None, "Client introuvable"

    # Vérifier que le véhicule existe et est disponible
    vehicules = vs.get_vehicules()
    vehicule = next((v for v in vehicules if v["id"] == vehicule_id), None)
    if vehicule is None:
        return None, "Véhicule introuvable"
    if not vehicule["disponible"]:
        return None, "Véhicule indisponible"

    locations = get_locations()
    location = {
        "id": generate_id(locations),
        "vehicule_id": vehicule_id,
        "client_id": client_id,
        "jours": jours
    }
    locations.append(location)
    sauvegarder_donnees(FICHIER_LOCATIONS, locations)
    vs.set_disponibilite(vehicule_id, False)
    return location, None


# 🔹 Retourner un véhicule
def retourner_vehicule(location_id):
    locations = get_locations()
    loc = next((l for l in locations if l["id"] == location_id), None)
    if loc is None:
        return False, "Location introuvable"
    vs.set_disponibilite(loc["vehicule_id"], True)
    locations.remove(loc)
    sauvegarder_donnees(FICHIER_LOCATIONS, locations)
    return True, None


# 🔹 Voir toutes les locations
def voir_locations():
    return get_locations()


# 🔹 Locations d'un client
def locations_par_client(client_id):
    return [loc for loc in get_locations() if loc["client_id"] == client_id]


# 🔹 Top véhicules loués
def top_vehicules():
    compteur = {}
    for loc in get_locations():
        vid = loc["vehicule_id"]
        compteur[vid] = compteur.get(vid, 0) + 1
    return sorted(compteur.items(), key=lambda x: x[1], reverse=True)


# 🔹 Calcul prix total
def calcul_prix(vehicule_id, jours):
    for v in vs.get_vehicules():
        if v["id"] == vehicule_id:
            return v["prix_par_jour"] * jours
    return 0


# 🔹 Total gains agence
def total_gains():
    return sum(calcul_prix(loc["vehicule_id"], loc["jours"]) for loc in get_locations())
