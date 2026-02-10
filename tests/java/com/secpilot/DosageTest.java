package com.secpilot;

import com.secpilot.healthcare.Dosage;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Date;

/**
 * Tests unitaires pour le module de dosage médical
 */
class DosageTest {

    @Test
    @DisplayName("Calcule un dosage normal dans les limites")
    void testNormalDosage() {
        // 50kg à 20mg/kg = 1000mg
        double result = Dosage.calculateDosage(50, 20, "paracetamol");
        assertEquals(1000, result, 0.01);
    }

    // TEST CONTEXTUEL : Règle métier - limite de dose maximale
    @Test
    @DisplayName("RÈGLE MÉTIER : Le dosage ne peut pas dépasser la limite maximale sûre")
    void testDosageCannotExceedMaximum() {
        /**
         * Contexte : Système de santé - la sécurité patient est critique
         * Les dosages ne doivent jamais dépasser les limites maximales sûres
         */
        // 150kg à 30mg/kg = 4500mg, mais max est 4000mg
        double result = Dosage.calculateDosage(150, 30, "paracetamol");
        assertTrue(result <= 4000,
            "Le dosage " + result + "mg dépasse le maximum sûr de 4000mg");
    }

    @Test
    @DisplayName("Le dosage devrait être plafonné au maximum, pas rejeté")
    void testDosageCappedAtMaximum() {
        // 200kg à 50mg/kg = 10000mg, devrait plafonner à 4000mg
        double result = Dosage.calculateDosage(200, 50, "paracetamol");
        assertEquals(4000, result, 0.01,
            "Le dosage devrait être plafonné à la limite maximale sûre");
    }

    // TEST BUG CLASSIQUE : Division par zéro
    @Test
    @DisplayName("BUG CLASSIQUE : Une fréquence nulle devrait lever une exception")
    void testZeroFrequencyHandling() {
        /**
         * Bug : Division par zéro quand frequency est 0
         */
        assertThrows(ArithmeticException.class, () -> {
            Dosage.splitDailyDose(1000, 0);
        });
    }

    // TEST BUG CLASSIQUE : Sensibilité à la casse
    @Test
    @DisplayName("BUG CLASSIQUE : Vérification d'interaction insensible à la casse")
    void testCaseInsensitiveDrugCheck() {
        /**
         * Bug : Comparaison sensible à la casse manque les interactions
         */
        assertTrue(Dosage.checkDrugInteraction("WARFARIN", "ASPIRIN"),
            "Devrait détecter l'interaction quelle que soit la casse");
        assertTrue(Dosage.checkDrugInteraction("Warfarin", "Aspirin"),
            "Devrait détecter l'interaction avec casse mixte");
    }

    // TEST BUG CLASSIQUE : NumberFormatException
    @Test
    @DisplayName("BUG CLASSIQUE : Gestion de chaîne de dosage invalide")
    void testInvalidDosageString() {
        /**
         * Bug : Pas de try-catch pour format de nombre invalide
         */
        assertThrows(NumberFormatException.class, () -> {
            Dosage.parseDosage("invalid");
        });
        // Ou devrait retourner une valeur par défaut sensée / lever IllegalArgumentException
    }

    // TEST BUG CLASSIQUE : Mutation de Date
    @Test
    @DisplayName("BUG CLASSIQUE : Mutation de Date dans calculateNextDoseTime")
    void testDateMutation() {
        /**
         * Bug : La méthode mute l'objet Date original
         */
        Date original = new Date();
        long originalTime = original.getTime();

        Dosage.calculateNextDoseTime(original, 4);

        assertEquals(originalTime, original.getTime(),
            "La date originale ne devrait pas être mutée");
    }

    // TEST BUG CLASSIQUE : Dépassement d'entier
    @Test
    @DisplayName("BUG CLASSIQUE : Dépassement d'entier dans la validation")
    void testIntegerOverflow() {
        /**
         * Bug : dose * multiplier pourrait dépasser Integer.MAX_VALUE
         */
        boolean result = Dosage.validateDosageRange(
            Integer.MAX_VALUE / 2, 3, Integer.MAX_VALUE);

        // Si dépassement, le résultat serait incorrectement true
        assertFalse(result, "Devrait détecter que la dose dépasse le maximum même avec dépassement");
    }
}
