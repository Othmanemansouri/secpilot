/**
 * Tests unitaires pour le module de tarification E-commerce
 */
const {
    calculateDiscount,
    applyCoupon,
    calculateCartTotal,
    formatPrice,
    setProductPrice
} = require('../../src/javascript/ecommerce/pricing');

describe('calculateDiscount', () => {
    test('calcule une remise basique correctement', () => {
        expect(calculateDiscount(100, 10)).toBe(90);
    });

    test('gère une remise nulle', () => {
        expect(calculateDiscount(100, 0)).toBe(100);
    });

    // TEST CONTEXTUEL : Règle métier - les prix ne peuvent pas être négatifs
    test('RÈGLE MÉTIER : le prix ne peut pas être négatif avec >100% de remise', () => {
        /**
         * Contexte : Plateforme e-commerce où les prix ne doivent jamais être négatifs
         */
        const result = calculateDiscount(100, 150);
        expect(result).toBeGreaterThanOrEqual(0);
    });

    test('une remise extrême devrait plafonner à zéro', () => {
        const result = calculateDiscount(50, 200);
        expect(result).toBeGreaterThanOrEqual(0);
    });
});

describe('applyCoupon', () => {
    const validCoupons = [
        { code: 'SAVE10', discount: 10 },
        { code: '123', discount: 5 }  // Chaîne qui ressemble à un nombre
    ];

    test('applique un coupon valide correctement', () => {
        expect(applyCoupon(100, 'SAVE10', validCoupons)).toBe(90);
    });

    // TEST BUG CLASSIQUE : Coercition de type avec ==
    test('BUG CLASSIQUE : comparaison d\'égalité stricte pour les codes coupon', () => {
        /**
         * Bug : Utiliser == au lieu de === peut causer des problèmes de coercition
         * Le code '123' ne devrait pas correspondre au nombre 123
         */
        const result = applyCoupon(100, 123, validCoupons);  // Nombre, pas chaîne
        expect(result).toBe(100);  // Ne devrait PAS appliquer la remise
    });
});

describe('setProductPrice', () => {
    test('définit un prix positif valide', () => {
        const product = { name: 'Widget', price: 10 };
        const result = setProductPrice(product, 25);
        expect(result.price).toBe(25);
    });

    // TEST CONTEXTUEL : Règle métier - les prix ne peuvent pas être négatifs
    test('RÈGLE MÉTIER : rejette un prix négatif', () => {
        /**
         * Contexte : La plateforme e-commerce interdit les prix négatifs
         */
        const product = { name: 'Widget', price: 10 };
        expect(() => setProductPrice(product, -5)).toThrow();
    });

    test('autorise le prix zéro pour les articles gratuits', () => {
        const product = { name: 'Widget', price: 10 };
        const result = setProductPrice(product, 0);
        expect(result.price).toBe(0);
    });
});

describe('formatPrice', () => {
    test('formate le prix avec deux décimales', () => {
        expect(formatPrice(19.99)).toBe('19.99 EUR');
    });

    // TEST BUG CLASSIQUE : toFixed retourne une string
    test('BUG CLASSIQUE : formatPrice devrait retourner un format utilisable', () => {
        const formatted = formatPrice(19.999);
        expect(formatted).toBe('20.00 EUR');  // Devrait arrondir correctement
    });
});
