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