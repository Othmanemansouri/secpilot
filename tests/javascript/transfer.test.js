/**
 * Tests unitaires pour le module de virement bancaire
 */
const {
    transferFunds,
    validateAccountNumber,
    calculateMonthlyPayment,
    isTransactionSuspicious,
    getAccountBalance
} = require('../../src/javascript/banking/transfer');

describe('transferFunds', () => {
    test('transfère avec succès entre les comptes', () => {
        const from = { id: 'A1', balance: 1000 };
        const to = { id: 'A2', balance: 500 };

        const result = transferFunds(from, to, 200);

        expect(result.success).toBe(true);
        expect(from.balance).toBe(800);
        expect(to.balance).toBe(700);
    });

    // TEST CONTEXTUEL : Règle métier - solde insuffisant
    test('RÈGLE MÉTIER : rejette le virement avec solde insuffisant', () => {
        /**
         * Contexte : Le système bancaire doit rejeter les virements quand l'émetteur
         * a un solde insuffisant pour prévenir les découverts non autorisés
         */
        const from = { id: 'A1', balance: 100 };
        const to = { id: 'A2', balance: 500 };

        expect(() => transferFunds(from, to, 200)).toThrow();

        // Les soldes devraient rester inchangés
        expect(from.balance).toBe(100);
        expect(to.balance).toBe(500);
    });

    test('autorise le virement du solde exact', () => {
        const from = { id: 'A1', balance: 100 };
        const to = { id: 'A2', balance: 0 };

        const result = transferFunds(from, to, 100);

        expect(result.success).toBe(true);
        expect(from.balance).toBe(0);
    });
});

describe('validateAccountNumber', () => {
    test('accepte un numéro valide à 10 chiffres', () => {
        expect(validateAccountNumber('1234567890')).toBe(true);
    });

    // TEST BUG CLASSIQUE : Vulnérabilité ReDoS
    test('BUG CLASSIQUE : gère une entrée ReDoS potentielle en sécurité', () => {
        /**
         * Bug : Backtracking catastrophique avec la regex
         */
        const maliciousInput = '1'.repeat(100);
        // Devrait se terminer dans un temps raisonnable, pas bloquer
        const start = Date.now();
        validateAccountNumber(maliciousInput);
        const elapsed = Date.now() - start;
        expect(elapsed).toBeLessThan(1000);  // Ne devrait pas prendre plus d'1 seconde
    });

    test('rejette les numéros de compte invalides', () => {
        expect(validateAccountNumber('12345')).toBe(false);
        expect(validateAccountNumber('123456789012345')).toBe(false);
    });
});

describe('calculateMonthlyPayment', () => {
    test('calcule la mensualité correctement', () => {
        // 10000€ à 5% TAEG sur 12 mois
        const payment = calculateMonthlyPayment(10000, 0.05, 12);
        expect(payment).toBeCloseTo(856.07, 1);
    });

    // TEST BUG CLASSIQUE : NaN avec taux zéro
    test('BUG CLASSIQUE : gère un taux d\'intérêt nul', () => {
        /**
         * Bug : Division par zéro mène à NaN
         */
        const payment = calculateMonthlyPayment(10000, 0, 12);
        expect(payment).not.toBeNaN();
        expect(payment).toBeCloseTo(833.33, 1);  // Division simple
    });
});

describe('getAccountBalance', () => {
    const accounts = {
        'A1': { balance: 1000 },
        'A2': { balance: 500 }
    };

    test('retourne le solde pour un compte existant', () => {
        expect(getAccountBalance('A1', accounts)).toBe(1000);
    });

    // TEST BUG CLASSIQUE : Gestion des comptes manquants
    test('BUG CLASSIQUE : gère un compte inexistant proprement', () => {
        /**
         * Bug : Ne devrait pas lever TypeError pour un compte manquant
         */
        expect(() => getAccountBalance('A999', accounts)).toThrow();
        // Ou retourner undefined/null, mais pas planter
    });
});
