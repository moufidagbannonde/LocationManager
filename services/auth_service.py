import bcrypt
from services.data_manager import charger_donnees, sauvegarder_donnees
from utils.generator import generate_id

FICHIER_CLIENTS = "data/clients.json"
FICHIER_ADMINS = "data/admins.json"


def hasher_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verifier_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())


# ── CLIENTS ──────────────────────────────────────────────

def inscrire_client(nom, email, password):
    clients = charger_donnees(FICHIER_CLIENTS)
    if any(c["email"] == email for c in clients):
        return None, "Email déjà utilisé"
    if not nom.strip() or not email.strip() or not password.strip():
        return None, "Tous les champs sont obligatoires"
    client = {
        "id": generate_id(clients),
        "nom": nom.strip(),
        "email": email.strip().lower(),
        "password": hasher_password(password)
    }
    clients.append(client)
    sauvegarder_donnees(FICHIER_CLIENTS, clients)
    return client, None


def connecter_client(email, password):
    clients = charger_donnees(FICHIER_CLIENTS)
    client = next((c for c in clients if c["email"] == email.strip().lower()), None)
    if client is None:
        return None, "Email introuvable"
    if not verifier_password(password, client["password"]):
        return None, "Mot de passe incorrect"
    return client, None


# ── ADMINS ───────────────────────────────────────────────

def connecter_admin(email, password):
    admins = charger_donnees(FICHIER_ADMINS)
    admin = next((a for a in admins if a["email"] == email.strip().lower()), None)
    if admin is None:
        return None, "Email introuvable"
    if not verifier_password(password, admin["password"]):
        return None, "Mot de passe incorrect"
    return admin, None


def creer_admin(nom, email, password):
    admins = charger_donnees(FICHIER_ADMINS)
    if any(a["email"] == email for a in admins):
        return None, "Email déjà utilisé"
    admin = {
        "id": generate_id(admins),
        "nom": nom.strip(),
        "email": email.strip().lower(),
        "password": hasher_password(password)
    }
    admins.append(admin)
    sauvegarder_donnees(FICHIER_ADMINS, admins)
    return admin, None
