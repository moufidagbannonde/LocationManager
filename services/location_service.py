from services.data_manager import charger_donnees, sauvegarder_donnees
import services.vehicule_service as vs
import services.client_service as cs
from utils.generator import generate_id

# Chemin du fichier JSON contenant les locations
FICHIER_LOCATIONS = "data/locations.json"


def get_locations():
    """
    Récupère toutes les locations enregistrées dans le fichier JSON.

    Returns:
        list: Liste des locations (chaque élément est un dictionnaire).
    """
    return charger_donnees(FICHIER_LOCATIONS)





# 🔹 Louer un véhicule
def louer_vehicule(client_id, vehicule_id, jours):
    """
    Permet de créer une location (louer un véhicule).

    Étapes:
    1. Vérifie si le client existe
    2. Vérifie si le véhicule existe et est disponible
    3. Crée une nouvelle location
    4. Sauvegarde la location
    5. Met le véhicule en indisponible

    Args:
        client_id (int): ID du client
        vehicule_id (int): ID du véhicule
        jours (int): Nombre de jours de location

    Returns:
        tuple:
            - dict: La location créée si succès
            - None: Sinon
            - str: Message d'erreur éventuel
    """

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

    # Création de la location
    locations = get_locations()
    location = {
        "id": generate_id(locations),  # ID unique
        "vehicule_id": vehicule_id,
        "client_id": client_id,
        "jours": jours,
        "statut": "en_cours"
    }

    # Ajout et sauvegarde
    locations.append(location)
    sauvegarder_donnees(FICHIER_LOCATIONS, locations)

    # Mise à jour de la disponibilité du véhicule
    vs.set_disponibilite(vehicule_id, False)

    return location, None


# 🔹 Retourner un véhicule
def retourner_vehicule(location_id):
    """
    Permet de retourner un véhicule (fin de location).

    Étapes:
    1. Vérifie si la location existe
    2. Rend le véhicule disponible
    3. Supprime la location
    4. Sauvegarde les modifications

    Args:
        location_id (int): ID de la location

    Returns:
        tuple:
            - bool: True si succès, False sinon
            - str: Message d'erreur éventuel
    """

    locations = get_locations()

    # Recherche de la location
    loc = next((l for l in locations if l["id"] == location_id), None)

    if loc is None:
        return False, "Location introuvable"

    # Remettre le véhicule disponible
    vs.set_disponibilite(loc["vehicule_id"], True)

    # Rendre la location terminée pour conserver un historique
    loc["statut"] = "terminee"
    sauvegarder_donnees(FICHIER_LOCATIONS, locations)

    return True, None


# 🔹 Voir toutes les locations
def voir_locations():
    """
    Retourne toutes les locations enregistrées.

    Returns:
        list: Liste complète des locations.
    """
    return [loc for loc in get_locations() if loc["statut"] == "en_cours"]


# 🔹 Locations d'un client
def locations_par_client(client_id):
    """
    Récupère toutes les locations associées à un client donné.

    Args:
        client_id (int): ID du client

    Returns:
        list: Liste des locations du client
    """
    return [loc for loc in get_locations() if loc["client_id"] == client_id]


# 🔹 Top véhicules loués
def top_vehicules():
    """
    Calcule les véhicules les plus loués.

    Fonctionnement:
    - Compte combien de fois chaque véhicule est loué
    - Trie les résultats par ordre décroissant

    Returns:
        list: Liste de tuples (vehicule_id, nombre_de_locations)
    """

    compteur = {}

    # Comptage des locations par véhicule
    for loc in get_locations():
        vid = loc["vehicule_id"]
        compteur[vid] = compteur.get(vid, 0) + 1

    # Tri du plus loué au moins loué
    return sorted(compteur.items(), key=lambda x: x[1], reverse=True)


# 🔹 Calcul prix total
def calcul_prix(vehicule_id, jours):
    """
    Calcule le prix total d'une location.

    Args:
        vehicule_id (int): ID du véhicule
        jours (int): Nombre de jours

    Returns:
        float|int: Prix total (0 si véhicule introuvable)
    """

    for v in vs.get_vehicules():
        if v["id"] == vehicule_id:
            return v["prix_par_jour"] * jours

    return 0  # Véhicule non trouvé


# 🔹 Total gains agence
def total_gains():
    """
    Calcule le total des gains générés par toutes les locations.

    Returns:
        float|int: Somme des revenus
    """

    return sum(
        calcul_prix(loc["vehicule_id"], loc["jours"])
        for loc in get_locations()
    )