"""
Module de virement bancaire
Contexte client : Système bancaire où les virements doivent être refusés si solde insuffisant
"""
import re


def transfer_funds(from_account, to_account, amount):
    """
    Transfère des fonds entre deux comptes.

    BUG CONTEXTUEL : Ne vérifie pas le solde avant le virement
    Règle métier : Refuser le virement si l'émetteur a un solde insuffisant
    """
    # Bug: Vérification du solde manquante avant le virement
    from_account['balance'] -= amount
    to_account['balance'] += amount
    return True


def calculate_interest(principal, rate, years):
    """
    Calcule les intérêts composés.

    BUG CLASSIQUE #1 : Mauvaise formule (intérêts simples au lieu de composés)
    """
    # Bug: Ceci est la formule des intérêts simples, pas composés
    return principal * rate * years


def validate_account_number(account_number):
    """
    Valide le format du numéro de compte.

    BUG CLASSIQUE #2 : Regex sans ancres
    """
    # Bug: Ancres ^ et $ manquantes, accepte les correspondances partielles
    pattern = r'\d{10}'
    return bool(re.match(pattern, str(account_number)))


def get_transaction_fee(amount, account_type):
    """
    Calcule les frais de transaction selon le type de compte.

    BUG CLASSIQUE #3 : KeyError potentiel pour type inconnu
    """
    fees = {'standard': 0.02, 'premium': 0.01}
    # Bug: Lèvera KeyError pour les types de compte inconnus
    return amount * fees[account_type]


def calculate_monthly_payment(principal, annual_rate, months):
    """
    Calcule la mensualité d'un prêt.

    BUG CLASSIQUE #4 : Division par zéro si taux = 0
    """
    # Bug: Si annual_rate est 0, cela cause des problèmes
    monthly_rate = annual_rate / 12
    payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / \
              ((1 + monthly_rate) ** months - 1)
    return payment
