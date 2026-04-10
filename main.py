from services.agence import Agence


def main():
    agence = Agence()

    print(" Système de location de véhicules (mode test)")

    while True:
        print("\n========== MENU ==========")
        print("1. Ajouter véhicule")
        print("2. Voir véhicules")
        print("3. Ajouter client")
        print("4. Voir clients")
        print("5. Louer véhicule")
        print("6. Retourner véhicule")
        print("7. Voir locations")
        print("8. Filtrer par prix")
        print("9. Véhicules les plus loués")
        print("0. Quitter")
        print("==========================")

        choix = input("Choix : ")

        # ---------------- VEHICULES ----------------
        if choix == "1":
            marque = input("Marque : ")
            modele = input("Modèle : ")
            prix = int(input("Prix par jour : "))

            v = agence.ajouter_vehicule(marque, modele, prix)
            print(" Véhicule ajouté :", v)

        elif choix == "2":
            print("\n Véhicules :")
            for v in agence.vehicules:
                print(v)

        # ---------------- CLIENTS ----------------
        elif choix == "3":
            nom = input("Nom client : ")
            c = agence.ajouter_client(nom)
            print(" Client ajouté :", c)

        elif choix == "4":
            print("\n Clients :")
            for c in agence.clients:
                print(c)

        # ---------------- LOCATIONS ----------------
        elif choix == "5":
            client_id = int(input("Client ID : "))
            vehicule_id = int(input("Véhicule ID : "))
            jours = int(input("Nombre de jours : "))

            location = agence.louer_vehicule(client_id, vehicule_id, jours)

            if location:
                print(" Location créée :", location)
            else:
                print(" Véhicule indisponible ou introuvable")

        elif choix == "6":
            location_id = int(input("Location ID : "))

            if agence.retourner_vehicule(location_id):
                print(" Véhicule retourné")
            else:
                print(" Location introuvable")

        elif choix == "7":
            print("\n Locations :")
            for l in agence.locations:
                print(l)

        # ---------------- LOGIQUE METIER ----------------
        elif choix == "8":
            max_prix = int(input("Prix maximum : "))
            result = agence.filtrer_par_prix(max_prix)

            print("\n Véhicules filtrés :")
            for v in result:
                print(v)

        elif choix == "9":
            print("\n Top véhicules loués :")
            print(agence.top_vehicules())

        # ---------------- QUITTER ----------------
        elif choix == "0":
            agence.sauvegarder()
            print(" Données sauvegardées. Fermeture du système...")
            break

        else:
            print(" Choix invalide")


if __name__ == "__main__":
    main()