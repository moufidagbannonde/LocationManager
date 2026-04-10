def generate_id(data):
    """
    Génère un nouvel ID unique pour une nouvelle location.

    Args:
        data (list): Liste des locations existantes.

    Returns:
        int: Nouvel ID incrémenté.
    """
    if not data:
        return 1  # Si aucune donnée, on commence à 1
    return max(item["id"] for item in data) + 1  # ID max + 1