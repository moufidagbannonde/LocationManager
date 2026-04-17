class Admin:
    def __init__(self, id, nom, email, password):
        self.id = id
        self.nom = nom
        self.email = email
        self.password = password

    def to_dict(self):
        return self.__dict__
