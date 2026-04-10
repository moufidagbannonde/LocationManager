from services.agence import Agence

def main():
    agence = Agence()

    while True:
        print("\n1. Ajouter véhicule")
        print("2. Voir véhicules")
        print("3. Ajouter client")
        print("4. Voir clients")
        print("5. Louer véhicule")
        print("6. Retourner véhicule")
        print("7. Voir locations")
        print("8. Filtrer par prix")
        print("9. Véhicules les plus loués")
        print("0. Quitter")

        choix = input("Choix : ")

        if choix == "0":
            break

if __name__ == "__main__":
    main()