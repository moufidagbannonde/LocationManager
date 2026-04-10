class Client:
    def __init__(self, id, nom):
        self.id = id
        self.nom = nom

    def to_dict(self):
        return self.__dict__