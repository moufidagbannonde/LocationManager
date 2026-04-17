from services.data_manager import charger_donnees, sauvegarder_donnees
from services.auth_service import hasher_password, verifier_password

FICHIER_CLIENTS = "data/clients.json"


def get_clients():
    return charger_donnees(FICHIER_CLIENTS)


def lister_clients():
    return get_clients()


def rechercher_client(nom):
    return [c for c in get_clients() if nom.lower() in c["nom"].lower()]


def modifier_client(client_id, nouveau_nom=None, nouvel_email=None):
    clients = get_clients()
    for c in clients:
        if c["id"] == client_id:
            if nouveau_nom and nouveau_nom.strip():
                c["nom"] = nouveau_nom.strip()
            if nouvel_email and nouvel_email.strip():
                if any(x["email"] == nouvel_email.strip().lower() and x["id"] != client_id for x in clients):
                    return None, "Email déjà utilisé"
                c["email"] = nouvel_email.strip().lower()
            sauvegarder_donnees(FICHIER_CLIENTS, clients)
            return c, None
    return None, "Client introuvable"


def changer_password(client_id, ancien_password, nouveau_password):
    clients = get_clients()
    for c in clients:
        if c["id"] == client_id:
            if not verifier_password(ancien_password, c["password"]):
                return False, "Ancien mot de passe incorrect"
            c["password"] = hasher_password(nouveau_password)
            sauvegarder_donnees(FICHIER_CLIENTS, clients)
            return True, None
    return False, "Client introuvable"


def supprimer_client(client_id):
    clients = get_clients()
    new_clients = [c for c in clients if c["id"] != client_id]
    if len(new_clients) == len(clients):
        return False
    sauvegarder_donnees(FICHIER_CLIENTS, new_clients)
    return True
