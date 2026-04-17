from utils.colors import VERT, ROUGE, JAUNE, CYAN, BLANC, MAGENTA, BLEU, GRIS, RESET
import services.vehicule_service as vs


def afficher_vehicule(v):
    dispo = f"{VERT}✅ Disponible{RESET}" if v["disponible"] else f"{ROUGE}❌ Indisponible{RESET}"
    print(f"  {CYAN}[{v['immatriculation']}]{RESET} {BLANC}{v['marque']} {v['modele']}{RESET} — {JAUNE}{v['prix_par_jour']:,.0f}/jour{RESET} — {dispo}")


def afficher_client(c):
    print(f"  {CYAN}[#{c['id']}]{RESET} {BLANC}{c['nom']}{RESET} — {GRIS}{c['email']}{RESET}")


def afficher_location(loc):
    if loc["statut"] == "en_cours":
        statut = f"{VERT}🟢 En cours{RESET}"
    else:
        statut = f"{GRIS}✅ Terminée{RESET}"

    date_debut = loc.get("date_debut", "N/A")
    date_fin   = loc.get("date_fin", "N/A")

    vehicule = vs.get_vehicule_par_immat(loc["immatriculation"])
    if vehicule:
        prix_total = f"{JAUNE}{vehicule['prix_par_jour'] * loc['jours']:,.0f}{RESET}"
    else:
        prix_total = f"{GRIS}N/A{RESET}"

    print(
        f"  {MAGENTA}[#{loc['id']}]{RESET} "
        f"{CYAN}{loc['immatriculation']}{RESET} | "
        f"{BLANC}{loc['jours']} jour(s){RESET} | "
        f"{GRIS}{date_debut} → {date_fin}{RESET} | "
        f"💰 {prix_total} | {statut}"
    )
