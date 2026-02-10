package com.secpilot.healthcare;

import java.util.Map;
import java.util.HashMap;
import java.util.Date;

/**
 * Module de dosage médical
 * Contexte client : Système médical où les dosages ne doivent pas dépasser les limites maximales
 */
public class Dosage {

    // Doses maximales sûres en mg
    private static final Map<String, Integer> MAX_DOSES = new HashMap<>();
    static {
        MAX_DOSES.put("paracetamol", 4000);
        MAX_DOSES.put("ibuprofen", 3200);
        MAX_DOSES.put("aspirin", 4000);
    }

    /**
     * Calcule le dosage de médicament basé sur le poids du patient.
     * BUG CONTEXTUEL : N'applique pas la limite de dose maximale
     * Règle métier : Le dosage ne doit jamais dépasser la limite maximale sûre
     */
    public static double calculateDosage(double weightKg, double dosePerKg, String medication) {
        // Bug: Validation de la dose maximale manquante - problème de sécurité critique
        return weightKg * dosePerKg;
    }

    /**
     * Obtient la dose maximale pour un médicament.
     */
    public static Integer getMaxDose(String medication) {
        return MAX_DOSES.get(medication.toLowerCase());
    }

    /**
     * Divise la dose journalière en doses individuelles.
     * BUG CLASSIQUE #1 : ArithmeticException pour division par zéro
     */
    public static double splitDailyDose(double totalDose, int frequency) {
        // Bug: Pas de vérification pour frequency = 0
        return totalDose / frequency;
    }

    /**
     * Vérifie les interactions médicamenteuses.
     * BUG CLASSIQUE #2 : Sensibilité à la casse et comparaison de String
     */
    public static boolean checkDrugInteraction(String drug1, String drug2) {
        String[][] dangerousPairs = {
            {"warfarin", "aspirin"},
            {"metformin", "alcohol"}
        };

        for (String[] pair : dangerousPairs) {
            // Bug: Comparaison sensible à la casse, devrait utiliser equalsIgnoreCase
            if ((pair[0].equals(drug1) && pair[1].equals(drug2)) ||
                (pair[0].equals(drug2) && pair[1].equals(drug1))) {
                return true;
            }
        }
        return false;
    }

    /**
     * Parse le dosage depuis une chaîne.
     * BUG CLASSIQUE #3 : NumberFormatException non gérée
     */
    public static int parseDosage(String dosageString) {
        // Bug: Pas de try-catch pour entrée invalide
        return Integer.parseInt(dosageString.replaceAll("[^0-9]", ""));
    }

    /**
     * Calcule l'heure de la prochaine dose.
     * BUG CLASSIQUE #4 : Mutation de Date (utilisation de méthodes dépréciées)
     */
    @SuppressWarnings("deprecation")
    public static Date calculateNextDoseTime(Date lastDoseTime, int intervalHours) {
        // Bug: Mute l'objet Date original, méthodes dépréciées
        lastDoseTime.setHours(lastDoseTime.getHours() + intervalHours);
        return lastDoseTime;
    }

    /**
     * Valide que le dosage est dans la plage.
     * BUG CLASSIQUE #5 : Dépassement d'entier potentiel
     */
    public static boolean validateDosageRange(int dose, int multiplier, int maxAllowed) {
        // Bug: dose * multiplier pourrait dépasser Integer.MAX_VALUE
        return (dose * multiplier) <= maxAllowed;
    }
}
