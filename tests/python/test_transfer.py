"""
Tests unitaires pour le module de virement bancaire
"""
import pytest
import sys
sys.path.insert(0, 'src/python')

from banking.transfer import (
    transfer_funds,
    calculate_interest,
    validate_account_number,
    get_transaction_fee
)


class TestTransferFunds:
    """Tests pour la fonction transfer_funds"""

    def test_successful_transfer(self):
        """Test de virement valide entre comptes"""
        from_acc = {'id': 'A1', 'balance': 1000}
        to_acc = {'id': 'A2', 'balance': 500}

        result = transfer_funds(from_acc, to_acc, 200)

        assert result == True
        assert from_acc['balance'] == 800
        assert to_acc['balance'] == 700

    # TEST CONTEXTUEL : Règle métier - solde insuffisant
    @pytest.mark.business_rule
    def test_reject_insufficient_balance(self):
        """
        RÈGLE MÉTIER : Refuser le virement si solde insuffisant
        Contexte : Le système bancaire doit prévenir les découverts
        """
        from_acc = {'id': 'A1', 'balance': 100}
        to_acc = {'id': 'A2', 'balance': 500}

        # Un virement supérieur au solde disponible devrait échouer
        with pytest.raises((ValueError, AssertionError, Exception)):
            transfer_funds(from_acc, to_acc, 200)

        # Les soldes devraient rester inchangés
        assert from_acc['balance'] == 100, "Le solde ne devrait pas changer en cas d'échec"
        assert to_acc['balance'] == 500, "Le solde du destinataire ne devrait pas changer"

    def test_exact_balance_transfer(self):
        """Virement de l'exact solde disponible"""
        from_acc = {'id': 'A1', 'balance': 100}
        to_acc = {'id': 'A2', 'balance': 0}

        result = transfer_funds(from_acc, to_acc, 100)

        assert result == True
        assert from_acc['balance'] == 0
        assert to_acc['balance'] == 100


class TestCalculateInterest:
    """Tests pour la fonction calculate_interest"""

    # TEST BUG CLASSIQUE : Intérêts simples vs composés
    @pytest.mark.classic_bug
    def test_compound_interest_calculation(self):
        """
        BUG CLASSIQUE : Utilise la formule des intérêts simples au lieu de composés
        """
        # 1000€ à 10% pendant 2 ans composés = 1000 * (1.1)^2 - 1000 = 210€
        result = calculate_interest(1000, 0.10, 2)
        expected_compound = 210.0
        assert abs(result - expected_compound) < 0.01, "Devrait utiliser la formule des intérêts composés"


class TestValidateAccountNumber:
    """Tests pour la fonction validate_account_number"""

    def test_valid_account_number(self):
        """Test numéro de compte valide à 10 chiffres"""
        assert validate_account_number("1234567890") == True

    # TEST BUG CLASSIQUE : Problème d'ancre regex
    @pytest.mark.classic_bug
    def test_reject_longer_number(self):
        """
        BUG CLASSIQUE : Regex sans ancres
        Devrait rejeter les numéros de plus de 10 chiffres
        """
        assert validate_account_number("12345678901234") == False

    def test_reject_shorter_number(self):
        """Devrait rejeter les numéros de moins de 10 chiffres"""
        assert validate_account_number("12345") == False


class TestGetTransactionFee:
    """Tests pour la fonction get_transaction_fee"""

    def test_standard_account_fee(self):
        """Le compte standard a 2% de frais"""
        result = get_transaction_fee(1000, 'standard')
        assert result == 20.0

    # TEST BUG CLASSIQUE : Gestion de clé manquante
    @pytest.mark.classic_bug
    def test_unknown_account_type(self):
        """
        BUG CLASSIQUE : KeyError pour types de compte inconnus
        Devrait gérer proprement, pas planter
        """
        # Ne devrait pas lever KeyError
        try:
            result = get_transaction_fee(1000, 'unknown_type')
            # Devrait retourner des frais par défaut ou lever une ValueError appropriée
            assert isinstance(result, (int, float))
        except KeyError:
            pytest.fail("Devrait gérer le type de compte inconnu proprement, pas lever KeyError")
