class Vehicule:
    def __init__(self, id, marque, modele, prix_par_jour, disponible=True):
        #  Identifiant unique du véhicule
        # Exemple : 1, 2, 3...
        self.id = id

        #  Marque du véhicule (Toyota, BMW...)
        self.marque = marque

        #  Modèle du véhicule (Corolla, X5...)
        self.modele = modele

        #  Prix de location par jour
        self.prix_par_jour = prix_par_jour

        #  Disponibilité du véhicule
        # True = disponible
        # False = déjà loué
        self.disponible = disponible

    def to_dict(self):
        """
        🔥 IMPORTANT POUR JSON

        Cette méthode transforme l'objet Python en dictionnaire
        pour pouvoir le sauvegarder dans un fichier JSON.

        Exemple :
        Vehicule -> {
            "id": 1,
            "marque": "Toyota",
            ...
        }

        self.__dict__ = tous les attributs de l'objet
        """
        return self.__dict__