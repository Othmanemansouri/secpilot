"""
Module de tarification E-commerce
Contexte client : Plateforme e-commerce où les prix ne doivent JAMAIS être négatifs
"""


def calculate_discount(original_price, discount_percent):
    """
    Calcule le prix après remise.

    BUG CLASSIQUE #1 : Pas de validation si remise > 100%
    BUG CONTEXTUEL : Peut retourner un prix négatif
    """
    # Bug: Pas de plafonnement de la remise, peut résulter en prix négatif
    discounted_amount = original_price * discount_percent / 100
    final_price = original_price - discounted_amount
    return final_price


def apply_bulk_discount(items, threshold=10):
    """
    Applique une remise de 15% si le nombre d'articles dépasse le seuil.

    BUG CLASSIQUE #2 : Erreur off-by-one (devrait être >= et non >)
    """
    total = sum(item['price'] for item in items)
    # Bug: Off-by-one, un seuil de 10 devrait inclure exactement 10 articles
    if len(items) > threshold:
        total = total * 0.85
    return total


def set_product_price(product, new_price):
    """
    Met à jour le prix d'un produit.

    BUG CONTEXTUEL : Pas de validation que le prix ne peut pas être négatif
    Règle métier : Les prix e-commerce ne doivent jamais être négatifs
    """
    # Bug: Validation de règle métier manquante
    product['price'] = new_price
    return product


def calculate_tax(price, tax_rate):
    """
    Calcule le prix avec taxe.

    BUG CLASSIQUE #3 : Problème de précision en virgule flottante
    """
    # Bug: Devrait utiliser Decimal pour les calculs financiers
    return price + (price * tax_rate)


def format_price(price):
    """
    Formate un prix pour l'affichage.

    BUG CLASSIQUE #4 : Pas d'arrondi correct
    """
    # Bug: round() peut avoir des comportements inattendus avec les floats
    return f"{price:.2f} EUR"
