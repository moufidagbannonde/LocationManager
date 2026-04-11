def afficher_vehicule(v):
    dispo = "✅ Disponible" if v["disponible"] else "❌ Indisponible"
    print(f"  [{v['id']}] {v['marque']} {v['modele']} — {v['prix_par_jour']} /jour — {dispo}")

def afficher_client(c):
    print(f"  [{c['id']}] {c['nom']}")

def afficher_location(loc):
    print(f"  [Location {loc['id']}] Client ID: {loc['client_id']} | Véhicule ID: {loc['vehicule_id']} | {loc['jours']} jour(s)")
