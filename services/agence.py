from services.data_manager import charger_donnees, sauvegarder_donnees






class Agence:
    def __init__(self):
        self.vehicules = charger_donnees("data/vehicules.json")
        self.clients = charger_donnees("data/clients.json")
        self.locations = charger_donnees("data/locations.json")

    def generate_id(self, data):
        if not data:
            return 1
        return max(item["id"] for item in data) + 1 
    def sauvegarder(self):
        sauvegarder_donnees("data/vehicules.json", self.vehicules)
        sauvegarder_donnees("data/clients.json", self.clients)
        sauvegarder_donnees("data/locations.json", self.locations)

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

                return location

        return None 
    
    
    def retourner_vehicule(self, location_id):
        for loc in self.locations:
            if loc["id"] == location_id:
                for v in self.vehicules:
                    if v["id"] == loc["vehicule_id"]:
                        v["disponible"] = True

                self.locations.remove(loc)
                return True

        return False

    def afficher_locations(self):
        return self.locations

    def calcul_prix(self, vehicule_id, jours):
        for v in self.vehicules:
            if v["id"] == vehicule_id:
                return v["prix_par_jour"] * jours
        return 0

    def top_vehicules(self):
        compteur = {}

        for loc in self.locations:
            vid = loc["vehicule_id"]
            compteur[vid] = compteur.get(vid, 0) + 1

        return sorted(compteur.items(), key=lambda x: x[1], reverse=True)

    def filtrer_par_prix(self, max_prix):
        result = []
        for v in self.vehicules:
            if v["prix_par_jour"] <= max_prix:
                result.append(v)

        return result

    def ajouter_client(self, nom):
        client = {
            "id": self.generate_id(self.clients),
            "nom": nom
        }

        self.clients.append(client)
        return client