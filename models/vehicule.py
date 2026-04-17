class Vehicule:
    def __init__(self, id, immatriculation, marque, modele, prix_par_jour, disponible=True):
        self.id = id
        self.immatriculation = immatriculation
        self.marque = marque
        self.modele = modele
        self.prix_par_jour = prix_par_jour
        self.disponible = disponible

    def to_dict(self):
        return self.__dict__
