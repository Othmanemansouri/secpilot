/**
 * Module de dosage médical
 * Contexte client : Système médical où les dosages ne doivent pas dépasser les limites maximales
 */

const MAX_DOSES = {
    paracetamol: 4000,  // mg par jour
    ibuprofen: 3200,    // mg par jour
    aspirin: 4000       // mg par jour
};

/**
 * Calcule le dosage de médicament basé sur le poids du patient
 * BUG CONTEXTUEL : N'applique pas la limite de dose maximale
 * Règle métier : Le dosage ne doit jamais dépasser la limite maximale sûre
 */
function calculateDosage(weightKg, dosePerKg, medication) {
    // Bug: Validation de la dose maximale manquante - problème de sécurité critique
    const calculatedDose = weightKg * dosePerKg;
    return calculatedDose;
}

/**
 * Parse le dosage depuis une chaîne de prescription
 * BUG CLASSIQUE #1 : parseInt sans radix
 */
function parseDosage(dosageString) {
    // Bug: parseInt sans radix peut donner des résultats inattendus
    // "08" serait interprété comme 0 en ancien JS (octal)
    return parseInt(dosageString);
}

/**
 * Vérifie si une dose est dans la plage sûre
 * BUG CLASSIQUE #2 : Opérateur de comparaison incorrect
 */
function isDoseSafe(dose, minDose, maxDose) {
    // Bug: Utilise < au lieu de <= pour la borne supérieure
    return dose >= minDose && dose < maxDose;
}

/**
 * Calcule l'heure de la prochaine dose
 * BUG CLASSIQUE #3 : Mutation de l'objet Date
 */
function calculateNextDoseTime(lastDoseTime, intervalHours) {
    // Bug: Mute l'objet Date original
    const nextDose = lastDoseTime;
    nextDose.setHours(nextDose.getHours() + intervalHours);
    return nextDose;
}

/**
 * Valide l'âge du patient pour un médicament
 * BUG CLASSIQUE #4 : Confusion truthy/falsy avec 0
 */
function validatePatientAge(age, minimumAge) {
    // Bug: age de 0 serait falsy et échouerait la validation
    if (!age) {
        return false;
    }
    return age >= minimumAge;
}

module.exports = {
    MAX_DOSES,
    calculateDosage,
    parseDosage,
    isDoseSafe,
    calculateNextDoseTime,
    validatePatientAge
};
