import services.auth_service as auth
import services.vehicule_service as vs
import services.location_service as ls
import services.client_service as cs
from services.display import afficher_vehicule, afficher_client, afficher_location
from utils.colors import (
    ok, erreur, warning, info, titre, section,
    VERT, ROUGE, JAUNE, CYAN, BLANC, MAGENTA, BLEU, GRIS, RESET
)


# ══════════════════════════════════════════════
#  MENU CLIENT
# ══════════════════════════════════════════════

def menu_profil(client):
    while True:
        titre(f"PROFIL — {client['nom']}")
        print(f"  {GRIS}Nom   :{RESET} {BLANC}{client['nom']}{RESET}")
        print(f"  {GRIS}Email :{RESET} {CYAN}{client['email']}{RESET}")
        section("OPTIONS")
        print(f"  {JAUNE}1.{RESET} Modifier nom / email")
        print(f"  {JAUNE}2.{RESET} Changer mot de passe")
        print(f"  {JAUNE}3.{RESET} Mes locations en cours")
        print(f"  {JAUNE}4.{RESET} Historique complet")
        print(f"\n  {ROUGE}0.{RESET} Retour")
        choix = input(f"\n{CYAN}Choix : {RESET}").strip()

        if choix == "1":
            nouveau_nom = input(f"Nouveau nom {GRIS}({client['nom']}){RESET} : ").strip()
            nouvel_email = input(f"Nouvel email {GRIS}({client['email']}){RESET} : ").strip()
            result, err = cs.modifier_client(client["id"], nouveau_nom or None, nouvel_email or None)
            if err:
                erreur(err)
            else:
                client.update(result)
                ok("Profil mis à jour")

        elif choix == "2":
            ancien = input("Ancien mot de passe : ")
            nouveau = input("Nouveau mot de passe : ")
            success, err = cs.changer_password(client["id"], ancien, nouveau)
            ok("Mot de passe modifié") if success else erreur(err)

        elif choix == "3":
            locs = ls.locations_en_cours_par_client(client["id"])
            if locs:
                info(f"{len(locs)} location(s) en cours")
                for l in locs:
                    afficher_location(l)
            else:
                warning("Aucune location en cours")

        elif choix == "4":
            locs = ls.locations_par_client(client["id"])
            if locs:
                info(f"{len(locs)} location(s) au total")
                for l in locs:
                    afficher_location(l)
            else:
                warning("Aucune location trouvée")

        elif choix == "0":
            break


def menu_client(client):
    while True:
        titre(f"ESPACE CLIENT — {client['nom']}")
        print(f"  {JAUNE}1.{RESET} Mon profil")
        print(f"  {JAUNE}2.{RESET} Voir véhicules disponibles")
        print(f"  {JAUNE}3.{RESET} Louer un véhicule")
        print(f"  {JAUNE}4.{RESET} Retourner un véhicule")
        print(f"  {JAUNE}5.{RESET} Filtrer par prix")
        print(f"\n  {ROUGE}0.{RESET} Déconnexion")
        choix = input(f"\n{CYAN}Choix : {RESET}").strip()

        if choix == "1":
            menu_profil(client)

        elif choix == "2":
            vs.vehicules_disponibles()

        elif choix == "3":
            immat = input(f"{CYAN}Immatriculation : {RESET}").strip()
            jours = input(f"{CYAN}Nombre de jours : {RESET}").strip()
            if not jours.isdigit():
                erreur("Nombre de jours invalide")
                continue
            location, err = ls.louer_vehicule(client["id"], immat, int(jours))
            if err:
                erreur(err)
            else:
                afficher_location(location)
                ok("Location enregistrée !")

        elif choix == "4":
            locs = ls.locations_en_cours_par_client(client["id"])
            if not locs:
                warning("Aucune location en cours")
                continue
            info("Vos locations en cours :")
            for l in locs:
                afficher_location(l)
            loc_id = input(f"{CYAN}ID de la location à retourner : {RESET}").strip()
            if not loc_id.isdigit():
                erreur("ID invalide")
                continue
            success, err = ls.retourner_vehicule(int(loc_id))
            ok("Véhicule retourné") if success else erreur(err)

        elif choix == "5":
            prix = input(f"{CYAN}Prix max par jour : {RESET}").strip()
            if not prix.replace(".", "").isdigit():
                erreur("Prix invalide")
                continue
            vs.filtrer_par_prix(float(prix))

        elif choix == "0":
            print(f"\n{JAUNE}👋 À bientôt, {client['nom']} !{RESET}")
            break


# ══════════════════════════════════════════════
#  MENU ADMIN
# ══════════════════════════════════════════════

def menu_admin(admin):
    while True:
        titre(f"ESPACE ADMIN — {admin['nom']}")
        section("VÉHICULES")
        print(f"  {JAUNE}1.{RESET} Ajouter un véhicule")
        print(f"  {JAUNE}2.{RESET} Lister tous les véhicules")
        print(f"  {JAUNE}3.{RESET} Modifier un véhicule")
        print(f"  {JAUNE}4.{RESET} Supprimer un véhicule")
        print(f"  {JAUNE}5.{RESET} Filtrer par prix")
        section("LOCATIONS")
        print(f"  {JAUNE}6.{RESET} Locations en cours")
        print(f"  {JAUNE}7.{RESET} Historique complet")
        print(f"  {JAUNE}8.{RESET} Top véhicules loués")
        print(f"  {JAUNE}9.{RESET} Total gains agence")
        section("CLIENTS")
        print(f" {JAUNE}10.{RESET} Lister les clients")
        print(f" {JAUNE}11.{RESET} Rechercher un client")
        print(f" {JAUNE}12.{RESET} Voir locations d'un client")
        print(f" {JAUNE}13.{RESET} Supprimer un client")
        section("ADMINS")
        print(f" {JAUNE}14.{RESET} Créer un admin")
        print(f"\n  {ROUGE}0.{RESET} Déconnexion")
        choix = input(f"\n{CYAN}Choix : {RESET}").strip()

        if choix == "1":
            immat = input(f"{CYAN}Immatriculation : {RESET}").strip()
            marque = input(f"{CYAN}Marque : {RESET}").strip()
            modele = input(f"{CYAN}Modèle : {RESET}").strip()
            prix = input(f"{CYAN}Prix par jour : {RESET}").strip()
            if not prix.replace(".", "").isdigit():
                erreur("Prix invalide")
                continue
            vs.ajouter_vehicule(immat, marque, modele, float(prix))

        elif choix == "2":
            vs.lister_vehicules()

        elif choix == "3":
            immat = input(f"{CYAN}Immatriculation : {RESET}").strip()
            marque = input("Nouvelle marque (vide = inchangé) : ").strip()
            modele = input("Nouveau modèle (vide = inchangé) : ").strip()
            prix = input("Nouveau prix (vide = inchangé) : ").strip()
            vs.modifier_vehicule(immat, marque or None, modele or None, float(prix) if prix else None)

        elif choix == "4":
            immat = input(f"{CYAN}Immatriculation à supprimer : {RESET}").strip()
            vs.supprimer_vehicule(immat)

        elif choix == "5":
            prix = input(f"{CYAN}Prix max par jour : {RESET}").strip()
            if not prix.replace(".", "").isdigit():
                erreur("Prix invalide")
                continue
            vs.filtrer_par_prix(float(prix))

        elif choix == "6":
            locs = ls.voir_locations()
            if locs:
                info(f"{len(locs)} location(s) en cours")
                for l in locs:
                    afficher_location(l)
            else:
                warning("Aucune location en cours")

        elif choix == "7":
            locs = ls.get_locations()
            if locs:
                info(f"{len(locs)} location(s) au total")
                for l in locs:
                    afficher_location(l)
            else:
                warning("Aucune location")

        elif choix == "8":
            top = ls.top_vehicules()
            if top:
                print(f"\n{JAUNE}🏆 Top véhicules loués :{RESET}")
                for immat, count in top:
                    print(f"  {CYAN}{immat}{RESET} → {BLANC}{count} location(s){RESET}")
            else:
                warning("Aucune donnée")

        elif choix == "9":
            gains = ls.total_gains()
            print(f"\n  {JAUNE}💰 Total gains : {VERT}{gains:,.0f}{RESET}")

        elif choix == "10":
            clients = cs.lister_clients()
            if clients:
                info(f"{len(clients)} client(s)")
                for c in clients:
                    afficher_client(c)
            else:
                warning("Aucun client")

        elif choix == "11":
            nom = input(f"{CYAN}Nom à rechercher : {RESET}").strip()
            results = cs.rechercher_client(nom)
            if results:
                for c in results:
                    afficher_client(c)
            else:
                warning("Aucun client trouvé")

        elif choix == "12":
            client_id = input(f"{CYAN}ID du client : {RESET}").strip()
            if not client_id.isdigit():
                erreur("ID invalide")
                continue
            locs = ls.locations_par_client(int(client_id))
            if locs:
                info(f"{len(locs)} location(s)")
                for l in locs:
                    afficher_location(l)
            else:
                warning("Aucune location pour ce client")

        elif choix == "13":
            client_id = input(f"{CYAN}ID du client à supprimer : {RESET}").strip()
            if not client_id.isdigit():
                erreur("ID invalide")
                continue
            if cs.supprimer_client(int(client_id)):
                ok("Client supprimé")
            else:
                erreur("Client introuvable")

        elif choix == "14":
            nom = input(f"{CYAN}Nom : {RESET}").strip()
            email = input(f"{CYAN}Email : {RESET}").strip()
            password = input(f"{CYAN}Mot de passe : {RESET}").strip()
            result, err = auth.creer_admin(nom, email, password)
            if err:
                erreur(err)
            else:
                ok(f"Admin créé — {result['email']}")

        elif choix == "0":
            print(f"\n{JAUNE}👋 Déconnexion, {admin['nom']} !{RESET}")
            break


# ══════════════════════════════════════════════
#  MENU DE DÉMARRAGE
# ══════════════════════════════════════════════

def menu_demarrage():
    while True:
        print(f"\n{CYAN}╔═══════════════════════════════════════════╗{RESET}")
        print(f"{CYAN}║{RESET}{BLANC}    SYSTÈME DE LOCATIONS DE VÉHICULES      {RESET}{CYAN}║{RESET}")
        print(f"{CYAN}╚═══════════════════════════════════════════╝{RESET}")
        print(f"\n  {JAUNE}1.{RESET} Se connecter {GRIS}(client){RESET}")
        print(f"  {JAUNE}2.{RESET} S'inscrire {GRIS}(client){RESET}")
        print(f"  {JAUNE}3.{RESET} Se connecter {MAGENTA}(admin){RESET}")
        print(f"\n  {ROUGE}0.{RESET} Quitter")
        choix = input(f"\n{CYAN}Choix : {RESET}").strip()

        if choix == "1":
            email = input(f"{CYAN}Email : {RESET}").strip()
            password = input(f"{CYAN}Mot de passe : {RESET}")
            client, err = auth.connecter_client(email, password)
            if err:
                erreur(err)
            else:
                ok(f"Bienvenue, {client['nom']} !")
                menu_client(client)

        elif choix == "2":
            nom = input(f"{CYAN}Nom : {RESET}").strip()
            email = input(f"{CYAN}Email : {RESET}").strip()
            password = input(f"{CYAN}Mot de passe : {RESET}")
            client, err = auth.inscrire_client(nom, email, password)
            if err:
                erreur(err)
            else:
                ok(f"Compte créé ! Bienvenue, {client['nom']} !")
                menu_client(client)

        elif choix == "3":
            email = input(f"{CYAN}Email admin : {RESET}").strip()
            password = input(f"{CYAN}Mot de passe : {RESET}")
            admin, err = auth.connecter_admin(email, password)
            if err:
                erreur(err)
            else:
                ok(f"Bienvenue, {admin['nom']} !")
                menu_admin(admin)

        elif choix == "0":
            print(f"\n{JAUNE}À bientôt !{RESET}\n")
            break


if __name__ == "__main__":
    menu_demarrage()
