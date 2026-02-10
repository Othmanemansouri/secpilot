"""
Module de dosage médical
Contexte client : Système médical où les dosages ne doivent pas dépasser les limites maximales
"""

# Doses maximales sûres en mg par jour
MAX_DOSES = {
    'paracetamol': 4000,
    'ibuprofen': 3200,
    'aspirin': 4000
}


def calculate_dosage(weight_kg, dose_per_kg, medication):
    """
    Calcule le dosage de médicament basé sur le poids du patient.

    BUG CONTEXTUEL : N'applique pas la limite de dose maximale
    Règle métier : Le dosage ne doit jamais dépasser la limite maximale sûre
    """
    # Bug: Validation de la dose maximale manquante
    calculated_dose = weight_kg * dose_per_kg
    return calculated_dose


def split_daily_dose(total_dose, frequency):
    """
    Divise la dose journalière en doses individuelles.

    BUG CLASSIQUE #1 : Division par zéro possible
    """
    # Bug: Pas de vérification pour frequency = 0
    return total_dose / frequency


def convert_units(value, from_unit, to_unit):
    """
    Convertit entre unités de dosage.

    BUG CLASSIQUE #2 : Matrice de conversion incomplète
    """
    conversions = {
        ('mg', 'g'): 0.001,
        ('g', 'mg'): 1000,
        # Bug: Conversions mcg manquantes
    }
    # Bug: Lèvera KeyError pour les conversions non supportées
    return value * conversions[(from_unit, to_unit)]


def check_drug_interaction(drug1, drug2):
    """
    Vérifie les interactions médicamenteuses dangereuses.

    BUG CLASSIQUE #3 : Sensibilité à la casse
    """
    dangerous_pairs = [
        ('warfarin', 'aspirin'),
        ('metformin', 'alcohol'),
    ]
    # Bug: Comparaison sensible à la casse
    return (drug1, drug2) in dangerous_pairs or (drug2, drug1) in dangerous_pairs


def validate_patient_age(age, minimum_age):
    """
    Valide l'âge du patient pour un médicament.

    BUG CLASSIQUE #4 : Confusion truthy/falsy avec 0
    """
    # Bug: age de 0 serait falsy et échouerait la validation
    if not age:
        return False
    return age >= minimum_age
