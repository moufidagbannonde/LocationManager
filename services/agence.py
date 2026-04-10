from services.data_manager import charger_donnees, sauvegarder_donnees
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
            print(v)

    # =============================
    # 🟢 VÉHICULES DISPONIBLES
    # =============================
    def vehicules_disponibles(self):
        """
        🔹 Filtre les véhicules disponibles uniquement
        """

        disponibles = [v for v in self.vehicules if v["disponible"]]

        for v in disponibles:
            print(v)

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
            print(v)

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