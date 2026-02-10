"""
Tests unitaires pour le module de tarification E-commerce
Teste les bugs classiques et les violations de règles métier
"""
import pytest
import sys
sys.path.insert(0, 'src/python')

from ecommerce.pricing import (
    calculate_discount,
    apply_bulk_discount,
    set_product_price,
    calculate_tax
)


class TestCalculateDiscount:
    """Tests pour la fonction calculate_discount"""

    def test_basic_discount(self):
        """Test de calcul de remise standard"""
        result = calculate_discount(100, 10)
        assert result == 90.0, "10% de remise sur 100€ devrait être 90€"

    def test_zero_discount(self):
        """Test sans remise"""
        result = calculate_discount(100, 0)
        assert result == 100.0, "0% de remise devrait retourner le prix original"

    def test_full_discount(self):
        """Test remise à 100%"""
        result = calculate_discount(100, 100)
        assert result == 0.0, "100% de remise devrait résulter en 0€"

    # TEST CONTEXTUEL : Règle métier - les prix ne peuvent pas être négatifs
    @pytest.mark.business_rule
    def test_discount_cannot_exceed_100_percent(self):
        """
        RÈGLE MÉTIER : Le prix ne peut pas être négatif
        Contexte : Plateforme e-commerce où les prix ne doivent jamais être négatifs
        """
        result = calculate_discount(100, 150)
        assert result >= 0, "Le prix ne devrait jamais être négatif même avec >100% de remise"

    @pytest.mark.business_rule
    def test_large_discount_still_non_negative(self):
        """Une remise extrême devrait toujours résulter en un prix non-négatif"""
        result = calculate_discount(50, 200)
        assert result >= 0, "200% de remise devrait plafonner à 0€, pas devenir négatif"


class TestBulkDiscount:
    """Tests pour la fonction apply_bulk_discount"""

    def test_below_threshold_no_discount(self):
        """Les articles sous le seuil n'ont pas de remise"""
        items = [{'price': 10} for _ in range(5)]
        result = apply_bulk_discount(items, threshold=10)
        assert result == 50.0, "5 articles ne devraient pas avoir de remise groupée"

    # TEST BUG CLASSIQUE : Erreur off-by-one
    @pytest.mark.classic_bug
    def test_exactly_at_threshold(self):
        """
        BUG CLASSIQUE : Erreur off-by-one
        Les articles exactement au seuil DEVRAIENT avoir la remise
        """
        items = [{'price': 10} for _ in range(10)]
        result = apply_bulk_discount(items, threshold=10)
        # 10 articles à 10€ = 100€, avec 15% de remise = 85€
        assert result == 85.0, "Exactement 10 articles devraient avoir 15% de remise groupée"

    def test_above_threshold_gets_discount(self):
        """Les articles au-dessus du seuil ont la remise"""
        items = [{'price': 10} for _ in range(15)]
        result = apply_bulk_discount(items, threshold=10)
        assert result == 127.5, "15 articles devraient avoir 15% de remise groupée"


class TestSetProductPrice:
    """Tests pour la fonction set_product_price"""

    def test_set_valid_price(self):
        """Définir un prix positif valide"""
        product = {'name': 'Widget', 'price': 10}
        result = set_product_price(product, 25)
        assert result['price'] == 25

    # TEST CONTEXTUEL : Règle métier - les prix ne peuvent pas être négatifs
    @pytest.mark.business_rule
    def test_reject_negative_price(self):
        """
        RÈGLE MÉTIER : Le prix ne peut pas être négatif
        Contexte : La plateforme e-commerce interdit les prix négatifs
        """
        product = {'name': 'Widget', 'price': 10}
        with pytest.raises((ValueError, AssertionError)):
            set_product_price(product, -5)

    def test_zero_price_allowed(self):
        """Le prix zéro devrait être autorisé (articles gratuits)"""
        product = {'name': 'Widget', 'price': 10}
        result = set_product_price(product, 0)
        assert result['price'] == 0


class TestCalculateTax:
    """Tests pour la fonction calculate_tax"""

    def test_basic_tax_calculation(self):
        """Test de calcul de taxe basique"""
        result = calculate_tax(100, 0.08)
        assert abs(result - 108.0) < 0.01, "8% de taxe sur 100€ devrait être 108€"

    # TEST BUG CLASSIQUE : Précision virgule flottante
    @pytest.mark.classic_bug
    def test_floating_point_precision(self):
        """
        BUG CLASSIQUE : Précision virgule flottante
        Les calculs financiers nécessitent une précision exacte
        """
        result = calculate_tax(19.99, 0.0725)
        # Attendu : 19.99 + 1.449275 = 21.439275, arrondi à 21.44
        assert round(result, 2) == 21.44, "Le calcul de taxe devrait maintenir la précision"
