/**
 * Tests unitaires pour le module de dosage médical
 */
const {
    MAX_DOSES,
    calculateDosage,
    parseDosage,
    isDoseSafe,
    calculateNextDoseTime,
    validatePatientAge
} = require('../../src/javascript/healthcare/dosage');

describe('calculateDosage', () => {
    test('calcule un dosage normal dans les limites', () => {
        // 50kg à 20mg/kg = 1000mg (dans la limite de 4000mg)
        const result = calculateDosage(50, 20, 'paracetamol');
        expect(result).toBe(1000);
    });

    // TEST CONTEXTUEL : Règle métier - limite de dose maximale
    test('RÈGLE MÉTIER : le dosage ne peut pas dépasser la limite maximale sûre', () => {
        /**
         * Contexte : Système de santé - la sécurité patient est critique
         * Les dosages ne doivent jamais dépasser les limites maximales sûres
         */
        // 150kg à 30mg/kg = 4500mg, mais max est 4000mg
        const result = calculateDosage(150, 30, 'paracetamol');
        expect(result).toBeLessThanOrEqual(MAX_DOSES.paracetamol);
    });

    test('plafonne les calculs extrêmement élevés au maximum', () => {
        // 200kg à 50mg/kg = 10000mg, devrait plafonner à 4000mg
        const result = calculateDosage(200, 50, 'paracetamol');
        expect(result).toBe(MAX_DOSES.paracetamol);
    });
});

describe('parseDosage', () => {
    test('parse une chaîne numérique simple', () => {
        expect(parseDosage('500')).toBe(500);
    });

    // TEST BUG CLASSIQUE : parseInt sans radix
    test('BUG CLASSIQUE : parseInt devrait utiliser radix 10', () => {
        /**
         * Bug : parseInt('08') sans radix pourrait retourner 0 en ancien JS
         */
        expect(parseDosage('08')).toBe(8);
        expect(parseDosage('09')).toBe(9);
    });
});

describe('isDoseSafe', () => {
    test('identifie une dose dans la plage', () => {
        expect(isDoseSafe(500, 100, 1000)).toBe(true);
    });

    // TEST BUG CLASSIQUE : Comparaison de borne
    test('BUG CLASSIQUE : une dose égale à maxDose devrait être sûre', () => {
        /**
         * Bug : Utilise < au lieu de <= pour la borne supérieure
         */
        expect(isDoseSafe(1000, 100, 1000)).toBe(true);  // Exactement au max
    });

    test('identifie une dose hors plage', () => {
        expect(isDoseSafe(50, 100, 1000)).toBe(false);   // Sous le min
        expect(isDoseSafe(1001, 100, 1000)).toBe(false); // Au-dessus du max
    });
});

describe('calculateNextDoseTime', () => {
    // TEST BUG CLASSIQUE : Mutation de Date
    test('BUG CLASSIQUE : ne devrait pas muter la Date originale', () => {
        /**
         * Bug : La fonction mute l'objet Date passé
         */
        const original = new Date('2024-01-01T08:00:00');
        const originalTime = original.getTime();

        calculateNextDoseTime(original, 4);

        // L'original devrait être inchangé
        expect(original.getTime()).toBe(originalTime);
    });

    test('calcule l\'heure de prochaine dose correctement', () => {
        const lastDose = new Date('2024-01-01T08:00:00');
        const nextDose = calculateNextDoseTime(new Date(lastDose), 4);

        expect(nextDose.getHours()).toBe(12);
    });
});

describe('validatePatientAge', () => {
    test('valide un âge adulte correctement', () => {
        expect(validatePatientAge(25, 18)).toBe(true);
    });

    // TEST BUG CLASSIQUE : Truthy/falsy avec 0
    test('BUG CLASSIQUE : un âge de 0 devrait être géré correctement', () => {
        /**
         * Bug : un âge de 0 est falsy et échouerait incorrectement la validation
         */
        // L'âge 0 est un âge valide (nouveau-né), ne devrait pas être traité comme manquant
        expect(validatePatientAge(0, 0)).toBe(true);  // Nouveau-né, âge min 0
    });

    test('rejette un âge sous le minimum', () => {
        expect(validatePatientAge(5, 18)).toBe(false);
    });
});
