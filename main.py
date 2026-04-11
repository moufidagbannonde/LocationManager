from services.display import afficher_location, afficher_client
import services.vehicule_service as vs
import services.location_service as ls
import services.client_service as cs


def main():   

    print("\n╔═══════════════════════════════════════════════════════╗")
    print("               SYSTÈME DE LOCATIONS DE VÉHICULES                     ")
    print("╚═══════════════════════════════════════════════════════╝")
            
    while True:    
            
        
            print("\n──────────── MENU PRINCIPAL ────────────")

            print("\n ************ VÉHICULES ************ \n")
            print("  1. Ajouter un véhicule")
            print("  2. Lister tous les véhicules")
            print("  3. Voir véhicules disponibles")
            print("  4. Modifier un véhicule")
            print("  5. Supprimer un véhicule")
            print("  6. Filtrer par prix")

            print("\n ************ LOCATIONS ************ \n")
            print("  7. Louer un véhicule")
            print("  8. Retourner un véhicule")
            print("  9. Historique des locations")
            print(" 10. Locations d’un client")
            print(" 11. Top véhicules les plus loués")
            print(" 12. Total des gains de l’agence")

            print("\n ************ CLIENTS ************ \n")
            print(" 13. Ajouter un client")
            print(" 14. Lister les clients")
            print(" 15. Rechercher un client")
            print(" 16. Modifier un client")
            print(" 17. Supprimer un client")

            print("\n0. Quitter")

            print("\n───────────────────────────────────────")

            choix = input("Choix : ")

            # ---------------- VÉHICULES ----------------
            if choix == "1":
                marque = input("Marque : ")
                modele = input("Modèle : ")
                prix = float(input("Prix par jour : "))
                vs.ajouter_vehicule(marque, modele, prix)

            elif choix == "2":
                vs.lister_vehicules()

            elif choix == "3":
                vs.vehicules_disponibles()

            elif choix == "4":
                vid = int(input("ID : "))
                marque = input("Nouvelle marque (vide si rien) : ")
                modele = input("Nouveau modèle (vide si rien) : ")
                prix = input("Nouveau prix (vide si rien) : ")
                vs.modifier_vehicule(vid, marque or None, modele or None, float(prix) if prix else None)

            elif choix == "5":
                vid = int(input("ID à supprimer : "))
                vs.supprimer_vehicule(vid)

            elif choix == "6":
                prix = float(input("Prix max : "))
                vs.filtrer_par_prix(prix)

            # ---------------- LOCATIONS ----------------
            elif choix == "7":
                client_id = int(input("Client ID : "))
                vehicule_id = int(input("Véhicule ID : "))
                jours = int(input("Nombre de jours : "))
                location, erreur = ls.louer_vehicule(client_id, vehicule_id, jours)
                if erreur:
                    print(f"❌ {erreur}")
                else:
                    prix = ls.calcul_prix(vehicule_id, jours)
                    afficher_location(location)
                    print(f"   💰 Prix total : {prix} ")

            elif choix == "8":
                location_id = int(input("Location ID : "))
                ok, erreur = ls.retourner_vehicule(location_id)
                if ok:
                    print("✅ Véhicule retourné")
                else:
                    print(f"❌ {erreur}")

            elif choix == "9":
                locs = ls.voir_locations()
                if locs:
                    print("\n Locations en cours :")
                    for l in locs:
                        afficher_location(l)
                else:
                    print("⚠️ Aucune location en cours")

            elif choix == "10":
                client_id = int(input("Client ID : "))
                locs = ls.locations_par_client(client_id)
                if locs:
                    print(f"\n Locations du client {client_id} :")
                    for l in locs:
                        afficher_location(l)
                else:
                    print("⚠️ Aucune location pour ce client")

            elif choix == "11":
                top = ls.top_vehicules()
                if top:
                    print("\n🏆 Top véhicules loués :")
                    for vid, count in top:
                        print(f"  Véhicule ID {vid} → {count} location(s)")
                else:
                    print("⚠️ Aucune donnée")

            elif choix == "12":
                print(f"\n💰 Total gains agence : {ls.total_gains()} ")

            # ---------------- CLIENTS ----------------
            elif choix == "13":
                nom = input("Nom du client : ")
                result, erreur = cs.ajouter_client(nom)
                if erreur:
                    print(f"❌ {erreur}")
                else:
                    print(f"✅ Client ajouté → ID: {result['id']} | Nom: {result['nom']}")

            elif choix == "14":
                clients = cs.lister_clients()
                if clients:
                    print("\n Clients :")
                    for c in clients:
                        afficher_client(c)
                else:
                    print("⚠️ Aucun client")

            elif choix == "15":
                nom = input("Nom à rechercher : ")
                results = cs.rechercher_client(nom)
                if results:
                    for c in results:
                        afficher_client(c)
                else:
                    print("⚠️ Aucun client trouvé")

            elif choix == "16":
                client_id = int(input("Client ID : "))
                nouveau_nom = input("Nouveau nom : ")
                result = cs.modifier_client(client_id, nouveau_nom)
                if result is None:
                    print("❌ Client introuvable")
                elif isinstance(result, str):
                    print(f"❌ {result}")
                else:
                    print(f"✅ Client modifié → ID: {result['id']} | Nom: {result['nom']}")

            elif choix == "17":
                client_id = int(input("Client ID : "))
                if cs.supprimer_client(client_id):
                    print("✅ Client supprimé")
                else:
                    print("❌ Client introuvable")

            elif choix == "0":
                break

            else:
                print("❌ Choix invalide")


if __name__ == "__main__":
    main()
