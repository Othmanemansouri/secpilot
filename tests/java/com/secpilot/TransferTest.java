package com.secpilot;

import com.secpilot.banking.Transfer;
import com.secpilot.banking.Transfer.Account;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

import java.math.BigDecimal;

/**
 * Tests unitaires pour le module de virement bancaire
 */
class TransferTest {

    @Test
    @DisplayName("Virement réussi entre comptes")
    void testSuccessfulTransfer() {
        Account from = new Account("A1", 1000);
        Account to = new Account("A2", 500);

        boolean result = Transfer.transferFunds(from, to, 200);

        assertTrue(result);
        assertEquals(800, from.getBalance(), 0.01);
        assertEquals(700, to.getBalance(), 0.01);
    }

    // TEST CONTEXTUEL : Règle métier - solde insuffisant
    @Test
    @DisplayName("RÈGLE MÉTIER : Rejette le virement avec solde insuffisant")
    void testRejectInsufficientBalance() {
        /**
         * Contexte : Le système bancaire doit rejeter les virements quand l'émetteur
         * a un solde insuffisant pour prévenir les découverts non autorisés
         */
        Account from = new Account("A1", 100);
        Account to = new Account("A2", 500);

        assertThrows(IllegalStateException.class, () -> {
            Transfer.transferFunds(from, to, 200);
        });

        // Les soldes devraient rester inchangés
        assertEquals(100, from.getBalance(), 0.01);
        assertEquals(500, to.getBalance(), 0.01);
    }

    @Test
    @DisplayName("Autorise le virement du solde exact")
    void testExactBalanceTransfer() {
        Account from = new Account("A1", 100);
        Account to = new Account("A2", 0);

        boolean result = Transfer.transferFunds(from, to, 100);

        assertTrue(result);
        assertEquals(0, from.getBalance(), 0.01);
        assertEquals(100, to.getBalance(), 0.01);
    }

    // TEST BUG CLASSIQUE : Null pointer
    @Test
    @DisplayName("BUG CLASSIQUE : Gestion du numéro de compte null")
    void testNullAccountNumber() {
        /**
         * Bug : Pas de vérification de null avant d'appeler des méthodes
         */
        assertThrows(NullPointerException.class, () -> {
            Transfer.validateAccountNumber(null);
        });
        // Mieux : devrait lever IllegalArgumentException avec message
    }

    // TEST BUG CLASSIQUE : Clé manquante dans HashMap
    @Test
    @DisplayName("BUG CLASSIQUE : Gestion du type de compte inconnu")
    void testUnknownAccountType() {
        /**
         * Bug : HashMap.get retourne null, puis l'unboxing cause NPE
         */
        assertThrows(Exception.class, () -> {
            Transfer.getTransactionFee(1000, "unknown_type");
        });
        // Devrait lever IllegalArgumentException, pas NullPointerException
    }

    // TEST BUG CLASSIQUE : BigDecimal equals vs compareTo
    @Test
    @DisplayName("BUG CLASSIQUE : Comparaison BigDecimal")
    void testBigDecimalComparison() {
        /**
         * Bug : equals() considère l'échelle, donc 2.0 != 2.00
         */
        BigDecimal amount1 = new BigDecimal("2.0");
        BigDecimal amount2 = new BigDecimal("2.00");

        assertTrue(Transfer.amountsEqual(amount1, amount2),
            "2.0 et 2.00 devraient être égaux à des fins financières");
    }
}
