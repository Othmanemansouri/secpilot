package com.secpilot.banking;

import java.math.BigDecimal;
import java.util.Map;
import java.util.HashMap;

/**
 * Module de virement bancaire
 * Contexte client : Système bancaire où les virements doivent être refusés si solde insuffisant
 */
public class Transfer {

    /**
     * Transfère des fonds entre comptes.
     * BUG CONTEXTUEL : Ne vérifie pas le solde avant le virement
     * Règle métier : Refuser le virement si l'émetteur a un solde insuffisant
     */
    public static boolean transferFunds(Account from, Account to, double amount) {
        // Bug: Vérification du solde manquante - violation critique de règle métier
        from.withdraw(amount);
        to.deposit(amount);
        return true;
    }

    /**
     * Calcule les intérêts composés.
     * BUG CLASSIQUE #1 : Utilisation de double pour les calculs financiers
     */
    public static double calculateInterest(double principal, double rate, int years) {
        // Bug: Devrait utiliser BigDecimal pour la précision financière
        return principal * Math.pow(1 + rate, years) - principal;
    }

    /**
     * Valide un numéro de compte.
     * BUG CLASSIQUE #2 : Vulnérabilité NullPointer
     */
    public static boolean validateAccountNumber(String accountNumber) {
        // Bug: Pas de vérification de null
        return accountNumber.matches("\\d{10}");
    }

    /**
     * Obtient les frais de transaction selon le type de compte.
     * BUG CLASSIQUE #3 : HashMap avec clé potentiellement manquante
     */
    public static double getTransactionFee(double amount, String accountType) {
        Map<String, Double> fees = new HashMap<>();
        fees.put("standard", 0.02);
        fees.put("premium", 0.01);

        // Bug: Lèvera NullPointerException pour les types de compte inconnus
        return amount * fees.get(accountType);
    }

    /**
     * Vérifie si deux montants sont égaux.
     * BUG CLASSIQUE #4 : Comparaison BigDecimal avec equals()
     */
    public static boolean amountsEqual(BigDecimal amount1, BigDecimal amount2) {
        // Bug: equals() considère l'échelle, donc 2.0 != 2.00
        // Devrait utiliser compareTo() == 0
        return amount1.equals(amount2);
    }

    /**
     * Classe interne pour Account
     */
    public static class Account {
        private String id;
        private double balance;

        public Account(String id, double balance) {
            this.id = id;
            this.balance = balance;
        }

        public String getId() { return id; }
        public double getBalance() { return balance; }
        public void withdraw(double amount) { balance -= amount; }
        public void deposit(double amount) { balance += amount; }
    }
}
