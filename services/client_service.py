from services.data_manager import charger_donnees, sauvegarder_donnees
from utils.generator import generate_id

FICHIER_CLIENTS = "data/clients.json"


def get_clients():
    return charger_donnees(FICHIER_CLIENTS)


# 🔹 Ajouter client
def ajouter_client(nom):
    if not nom.strip():
        return "Nom invalide"
    clients = get_clients()

    client = {
        "id": generate_id(clients),
        "nom": nom.strip()
    }

    clients.append(client)
    sauvegarder_donnees(FICHIER_CLIENTS, clients)
    return client, None


# 🔹 Lister clients
def lister_clients():
    return get_clients()


# 🔹 Rechercher client
def rechercher_client(nom):
    clients = get_clients()
    return [c for c in clients if nom.lower() in c["nom"].lower()]


# 🔹 Modifier client
def modifier_client(client_id, nouveau_nom):
    clients = get_clients()

    for c in clients:
        if c["id"] == client_id:
            if not nouveau_nom.strip():
                return "Nom invalide"
            c["nom"] = nouveau_nom.strip()
            sauvegarder_donnees(FICHIER_CLIENTS, clients)
            return c

    return None


# 🔹 Supprimer client
def supprimer_client(client_id):
    clients = get_clients()
    new_clients = [c for c in clients if c["id"] != client_id]

    if len(new_clients) == len(clients):
        return False

    sauvegarder_donnees(FICHIER_CLIENTS, new_clients)
    return True
