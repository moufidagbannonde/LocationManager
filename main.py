from services.agence import Agence


def main():
    agence = Agence()

    while True:
        print("\n1. Ajouter véhicule")
        print("2. Voir véhicules")
        print("3. Filtrer véhicules disponibles")
        print("4. Modifier véhicule")
        print("5. Supprimer véhicule")
        print("6. Filtrer par prix")
        print("0. Quitter")

        choix = input("Choix : ")

        if choix == "1":
            marque = input("Marque : ")
            modele = input("Modèle : ")
            prix = float(input("Prix par jour : "))

            agence.ajouter_vehicule(marque, modele, prix)

        elif choix == "2":
            agence.afficher_vehicules()

        elif choix == "3":
            agence.vehicules_disponibles()

        elif choix == "4":
            id = int(input("ID : "))
            marque = input("Nouvelle marque (vide si rien) : ")
            modele = input("Nouveau modèle : ")
            prix = input("Nouveau prix : ")

            prix = float(prix) if prix else None

            agence.modifier_vehicule(id, marque or None, modele or None, prix)

        elif choix == "5":
            id = int(input("ID à supprimer : "))
            agence.supprimer_vehicule(id)

        elif choix == "6":
            prix = float(input("Prix max : "))
            agence.filtrer_par_prix(prix)

        elif choix == "0":
            break

        else:
            print("❌ Choix invalide")


if __name__ == "__main__":
    main()