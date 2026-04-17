import json
import bcrypt
import random
import string


def gen_immat(seed):
    random.seed(seed)
    l1 = ''.join(random.choices(string.ascii_uppercase, k=2))
    n = str(random.randint(100, 999))
    l2 = ''.join(random.choices(string.ascii_uppercase, k=2))
    return f"{l1}-{n}-{l2}"


# Migrer vehicules.json
with open("data/vehicules.json", "r", encoding="utf-8") as f:
    vehicules = json.load(f)

immatriculations = set()
for i, v in enumerate(vehicules):
    seed = i * 7 + 13
    immat = gen_immat(seed)
    while immat in immatriculations:
        seed += 1
        immat = gen_immat(seed)
    immatriculations.add(immat)
    v["immatriculation"] = immat

with open("data/vehicules.json", "w", encoding="utf-8") as f:
    json.dump(vehicules, f, indent=4, ensure_ascii=False)

print(f"OK: {len(vehicules)} vehicules mis a jour avec immatriculations")

# Creer admins.json
pwd = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
admins = [{"id": 1, "nom": "Admin", "email": "admin@location.com", "password": pwd}]

with open("data/admins.json", "w", encoding="utf-8") as f:
    json.dump(admins, f, indent=4)

print("OK: admins.json cree — admin@location.com / admin123")
