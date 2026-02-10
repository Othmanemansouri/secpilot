package com.secpilot.ecommerce;

import java.util.List;

/**
 * Module de tarification E-commerce
 * Contexte client : Plateforme e-commerce où les prix ne doivent JAMAIS être négatifs
 */
public class Pricing {

    /**
     * Calcule le prix après remise.
     * BUG CLASSIQUE #1 : Troncature de division entière
     * BUG CONTEXTUEL : Pas de validation pour résultat négatif
     */
    public static double calculateDiscount(double originalPrice, int discountPercent) {
        // Bug: Division entière avant conversion en double
        double discountAmount = originalPrice * (discountPercent / 100);
        return originalPrice - discountAmount;
    }

    /**
     * Applique une remise groupée basée sur la quantité.
     * BUG CLASSIQUE #2 : Erreur off-by-one
     */
    public static double applyBulkDiscount(List<Product> items, int threshold) {
        double total = items.stream()
            .mapToDouble(Product::getPrice)
            .sum();

        // Bug: Devrait être >= et non >
        if (items.size() > threshold) {
            total *= 0.85;
        }
        return total;
    }

    /**
     * Définit le prix d'un produit.
     * BUG CONTEXTUEL : Pas de validation que le prix ne peut pas être négatif
     * Règle métier : Les prix e-commerce ne doivent jamais être négatifs
     */
    public static void setProductPrice(Product product, double newPrice) {
        // Bug: Validation de règle métier manquante
        product.setPrice(newPrice);
    }

    /**
     * Compare les prix pour égalité.
     * BUG CLASSIQUE #3 : Comparaison de virgule flottante
     */
    public static boolean pricesEqual(double price1, double price2) {
        // Bug: Comparaison directe de valeurs en virgule flottante
        return price1 == price2;
    }

    /**
     * Calcule le prix avec taxe.
     * BUG CLASSIQUE #4 : Concaténation de String dans une boucle (bug de performance)
     */
    public static String generatePriceReport(List<Product> products, double taxRate) {
        String report = "";
        for (Product p : products) {
            // Bug: La concaténation de String dans une boucle est inefficace
            report += p.getName() + ": " + (p.getPrice() * (1 + taxRate)) + " EUR\n";
        }
        return report;
    }

    /**
     * Classe interne pour Product
     */
    public static class Product {
        private String name;
        private double price;

        public Product(String name, double price) {
            this.name = name;
            this.price = price;
        }

        public String getName() { return name; }
        public double getPrice() { return price; }
        public void setPrice(double price) { this.price = price; }
    }
}
