package com.secpilot;

import com.secpilot.ecommerce.Pricing;
import com.secpilot.ecommerce.Pricing.Product;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Arrays;
import java.util.List;

/**
 * Tests unitaires pour le module de tarification E-commerce
 */
class PricingTest {

    @Test
    @DisplayName("Calcule une remise basique correctement")
    void testBasicDiscount() {
        double result = Pricing.calculateDiscount(100.0, 10);
        assertEquals(90.0, result, 0.01);
    }

    // TEST BUG CLASSIQUE : Division entière
    @Test
    @DisplayName("BUG CLASSIQUE : Troncature de division entière")
    void testIntegerDivisionBug() {
        /**
         * Bug : discountPercent / 100 utilise la division entière
         * 10 / 100 = 0 en arithmétique entière
         */
        double result = Pricing.calculateDiscount(100.0, 10);
        assertNotEquals(100.0, result, "La remise devrait être appliquée, pas zéro");
        assertEquals(90.0, result, 0.01, "10% de remise sur 100€ devrait être 90€");
    }

    // TEST CONTEXTUEL : Règle métier - les prix ne peuvent pas être négatifs
    @Test
    @DisplayName("RÈGLE MÉTIER : Le prix ne peut pas être négatif avec >100% de remise")
    void testPriceCannotBeNegative() {
        /**
         * Contexte : Plateforme e-commerce où les prix ne doivent jamais être négatifs
         */
        double result = Pricing.calculateDiscount(100.0, 150);
        assertTrue(result >= 0, "Le prix ne devrait jamais être négatif");
    }

    // TEST BUG CLASSIQUE : Erreur off-by-one
    @Test
    @DisplayName("BUG CLASSIQUE : Off-by-one dans le seuil de remise groupée")
    void testBulkDiscountAtExactThreshold() {
        /**
         * Bug : Utilise > au lieu de >= pour la vérification du seuil
         */
        List<Product> items = Arrays.asList(
            new Product("A", 10), new Product("B", 10),
            new Product("C", 10), new Product("D", 10),
            new Product("E", 10), new Product("F", 10),
            new Product("G", 10), new Product("H", 10),
            new Product("I", 10), new Product("J", 10)
        );

        double result = Pricing.applyBulkDiscount(items, 10);
        // 10 articles à 10€ = 100€, avec 15% de remise = 85€
        assertEquals(85.0, result, 0.01, "Exactement 10 articles devraient avoir la remise groupée");
    }

    // TEST CONTEXTUEL : Règle métier - prix négatif
    @Test
    @DisplayName("RÈGLE MÉTIER : setProductPrice rejette les prix négatifs")
    void testSetProductPriceRejectsNegative() {
        /**
         * Contexte : La plateforme e-commerce interdit les prix négatifs
         */
        Product product = new Product("Widget", 10);

        assertThrows(IllegalArgumentException.class, () -> {
            Pricing.setProductPrice(product, -5);
        });
    }

    // TEST BUG CLASSIQUE : Comparaison de virgule flottante
    @Test
    @DisplayName("BUG CLASSIQUE : Comparaison de virgule flottante")
    void testFloatingPointComparison() {
        /**
         * Bug : Comparaison directe == de valeurs en virgule flottante
         */
        double price1 = 0.1 + 0.2;
        double price2 = 0.3;

        // Ceci démontre le bug - ceux-ci devraient être "égaux" pour la tarification
        assertTrue(Pricing.pricesEqual(price1, price2),
            "0.1 + 0.2 devrait être égal à 0.3 à des fins pratiques");
    }
}
