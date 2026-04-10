from services.data_manager import charger_donnees, sauvegarder_donnees
from services.display import afficher_vehicule, afficher_location
from models.vehicule import Vehicule


class Agence:
    def __init__(self):
        """
        🔥 Au démarrage du programme :
        - on charge tous les fichiers JSON en mémoire
        """

        self.vehicules = charger_donnees("data/vehicules.json")
        self.clients = charger_donnees("data/clients.json")
        self.locations = charger_donnees("data/locations.json")

    # =============================
    # 🔧 GÉNÉRATION D'ID
    # =============================
    def generate_id(self, data):
        """
        🔹 Génère un ID unique automatiquement

        LOGIQUE :
        - Si liste vide → retourne 1
        - Sinon → max(id) + 1

        👉 Exemple :
        [1,2,3] → retourne 4
        """

        if not data:
            return 1

        return max(item["id"] for item in data) + 1

    # =============================
    # 🚗 AJOUTER UN VÉHICULE
    # =============================
    def ajouter_vehicule(self, marque, modele, prix):
        """
        🔹 Crée un nouveau véhicule et le sauvegarde
        """

        nouvel_id = self.generate_id(self.vehicules)

        # Création objet
        vehicule = Vehicule(nouvel_id, marque, modele, prix)

        # Conversion en dictionnaire pour JSON
        self.vehicules.append(vehicule.to_dict())

        # Sauvegarde dans fichier
        sauvegarder_donnees("data/vehicules.json", self.vehicules)

        print("✅ Véhicule ajouté avec succès !")

    # =============================
    # 📄 LISTER TOUS LES VÉHICULES
    # =============================
    def afficher_vehicules(self):
        """
        🔹 Affiche tous les véhicules
        """

        if not self.vehicules:
            print("⚠️ Aucun véhicule trouvé")
            return

        for v in self.vehicules:
            afficher_vehicule(v)

    # =============================
    # 🟢 VÉHICULES DISPONIBLES
    # =============================
    def vehicules_disponibles(self):
        """
        🔹 Filtre les véhicules disponibles uniquement
        """

        disponibles = [v for v in self.vehicules if v["disponible"]]

        for v in disponibles:
            afficher_vehicule(v)

    # =============================
    # ✏️ MODIFIER VÉHICULE
    # =============================
    def modifier_vehicule(self, id, marque=None, modele=None, prix=None):
        """
        🔹 Modifie un véhicule existant

        👉 On modifie seulement les champs fournis
        """

        for v in self.vehicules:
            if v["id"] == id:

                if marque:
                    v["marque"] = marque

                if modele:
                    v["modele"] = modele

                if prix:
                    v["prix_par_jour"] = prix

                sauvegarder_donnees("data/vehicules.json", self.vehicules)
                print("✅ Véhicule modifié")
                return

        print("❌ Véhicule non trouvé")

    # =============================
    # ❌ SUPPRIMER VÉHICULE
    # =============================
    def supprimer_vehicule(self, id):
        """
        🔹 Supprime un véhicule
        """

        self.vehicules = [v for v in self.vehicules if v["id"] != id]

        sauvegarder_donnees("data/vehicules.json", self.vehicules)

        print("✅ Véhicule supprimé")

    # =============================
    # 🟡 FILTRER PAR PRIX
    # =============================
    def filtrer_par_prix(self, prix_max):
        """
        🔹 Retourne les véhicules dont le prix <= prix_max
        """

        result = [v for v in self.vehicules if v["prix_par_jour"] <= prix_max]

        for v in result:
            afficher_vehicule(v)

    # =============================
    # 🔴 LOGIQUE MÉTIER DISPONIBILITÉ
    # =============================
    def rendre_indisponible(self, id):
        """
        🔹 Appelé lors d'une location
        """

        for v in self.vehicules:
            if v["id"] == id:
                v["disponible"] = False

        sauvegarder_donnees("data/vehicules.json", self.vehicules)

    def rendre_disponible(self, id):
        """
        🔹 Appelé lors du retour véhicule
        """

        for v in self.vehicules:
            if v["id"] == id:
                v["disponible"] = True

        sauvegarder_donnees("data/vehicules.json", self.vehicules)

    # =============================
    # 📦 GESTION DES LOCATIONS
    # =============================
    def louer_vehicule(self, client_id, vehicule_id, jours):
        for v in self.vehicules:
            if v["id"] == vehicule_id and v["disponible"]:
                location = {
                    "id": self.generate_id(self.locations),
                    "vehicule_id": vehicule_id,
                    "client_id": client_id,
                    "jours": jours
                }
                v["disponible"] = False
                self.locations.append(location)
                sauvegarder_donnees("data/locations.json", self.locations)
                sauvegarder_donnees("data/vehicules.json", self.vehicules)
                return location
        return None

    def retourner_vehicule(self, location_id):
        for loc in self.locations:
            if loc["id"] == location_id:
                for v in self.vehicules:
                    if v["id"] == loc["vehicule_id"]:
                        v["disponible"] = True
                self.locations.remove(loc)
                sauvegarder_donnees("data/locations.json", self.locations)
                sauvegarder_donnees("data/vehicules.json", self.vehicules)
                return True
        return False

    def voir_locations(self):
        return self.locations

    def locations_par_client(self, client_id):
        return [loc for loc in self.locations if loc["client_id"] == client_id]

    # =============================
    # 📊 STATISTIQUES
    # =============================
    def top_vehicules(self):
        compteur = {}
        for loc in self.locations:
            vid = loc["vehicule_id"]
            compteur[vid] = compteur.get(vid, 0) + 1
        return sorted(compteur.items(), key=lambda x: x[1], reverse=True)

    # =============================
    # 💰 CALCULS
    # =============================
    def calcul_prix(self, vehicule_id, jours):
        for v in self.vehicules:
            if v["id"] == vehicule_id:
                return v["prix_par_jour"] * jours
        return 0

    def total_gains(self):
        return sum(self.calcul_prix(loc["vehicule_id"], loc["jours"]) for loc in self.locations)
    
    