class Location:
    def __init__(self, id, vehicule_id, client_id, jours, statut="en_cours"):
        self.id = id
        self.vehicule_id = vehicule_id
        self.client_id = client_id
        self.jours = jours
        self.statut = statut

    def to_dict(self):
        return self.__dict__