"""
Tests unitaires pour le module de dosage médical
"""
import pytest
import sys
sys.path.insert(0, 'src/python')

from healthcare.dosage import (
    calculate_dosage,
    split_daily_dose,
    convert_units,
    check_drug_interaction,
    MAX_DOSES
)


class TestCalculateDosage:
    """Tests pour la fonction calculate_dosage"""

    def test_normal_dosage_calculation(self):
        """Test de calcul de dosage normal dans les limites"""
        # Patient de 50kg à 20mg/kg = 1000mg (dans la limite de 4000mg)
        result = calculate_dosage(50, 20, 'paracetamol')
        assert result == 1000

    # TEST CONTEXTUEL : Règle métier - limite de dose maximale
    @pytest.mark.business_rule
    def test_dosage_cannot_exceed_maximum(self):
        """
        RÈGLE MÉTIER : Le dosage ne doit pas dépasser la limite maximale sûre
        Contexte : Système de santé - sécurité patient critique
        """
        # Patient de 150kg à 30mg/kg = 4500mg, mais max est 4000mg
        result = calculate_dosage(150, 30, 'paracetamol')
        assert result <= MAX_DOSES['paracetamol'], \
            f"Le dosage {result}mg dépasse le maximum sûr de {MAX_DOSES['paracetamol']}mg"

    @pytest.mark.business_rule
    def test_dosage_capped_at_maximum(self):
        """Le dosage devrait être plafonné, pas juste rejeté"""
        # Patient de 200kg à 50mg/kg = 10000mg, devrait plafonner à 4000mg
        result = calculate_dosage(200, 50, 'paracetamol')
        assert result == MAX_DOSES['paracetamol'], \
            "Le dosage devrait être plafonné à la limite maximale sûre"


class TestSplitDailyDose:
    """Tests pour la fonction split_daily_dose"""

    def test_normal_split(self):
        """Test de fractionnement de dose normal"""
        result = split_daily_dose(1000, 4)
        assert result == 250

    # TEST BUG CLASSIQUE : Division par zéro
    @pytest.mark.classic_bug
    def test_zero_frequency_raises_error(self):
        """
        BUG CLASSIQUE : Division par zéro
        Une fréquence de 0 devrait lever une erreur appropriée
        """
        with pytest.raises((ZeroDivisionError, ValueError)):
            split_daily_dose(1000, 0)


class TestConvertUnits:
    """Tests pour la fonction convert_units"""

    def test_mg_to_g(self):
        """Conversion milligrammes vers grammes"""
        result = convert_units(1000, 'mg', 'g')
        assert result == 1.0

    # TEST BUG CLASSIQUE : Matrice de conversion incomplète
    @pytest.mark.classic_bug
    def test_mcg_conversion_supported(self):
        """
        BUG CLASSIQUE : Matrice de conversion incomplète
        Devrait supporter les conversions de microgrammes
        """
        try:
            result = convert_units(1000, 'mcg', 'mg')
            assert result == 1.0  # 1000mcg = 1mg
        except KeyError:
            pytest.fail("Devrait supporter la conversion mcg vers mg")


class TestCheckDrugInteraction:
    """Tests pour la fonction check_drug_interaction"""

    def test_known_dangerous_pair(self):
        """Détecte une combinaison dangereuse connue"""
        assert check_drug_interaction('warfarin', 'aspirin') == True

    def test_reverse_order_detection(self):
        """Devrait détecter quel que soit l'ordre"""
        assert check_drug_interaction('aspirin', 'warfarin') == True

    # TEST BUG CLASSIQUE : Sensibilité à la casse
    @pytest.mark.classic_bug
    def test_case_insensitive_detection(self):
        """
        BUG CLASSIQUE : Sensibilité à la casse
        Les noms de médicaments devraient correspondre quelle que soit la casse
        """
        assert check_drug_interaction('WARFARIN', 'ASPIRIN') == True
        assert check_drug_interaction('Warfarin', 'Aspirin') == True
