/**
 * Module de tarification E-commerce
 * Contexte client : Plateforme e-commerce où les prix ne doivent JAMAIS être négatifs
 */

/**
 * Calcule le prix après remise
 * BUG CLASSIQUE #1 : Problème de précision en virgule flottante
 * BUG CONTEXTUEL : Pas de validation pour résultat négatif
 */
function calculateDiscount(originalPrice, discountPercent) {
    // Bug: Pas de validation, peut retourner un prix négatif
    const discountAmount = originalPrice * (discountPercent / 100);
    return originalPrice - discountAmount;
}

/**
 * Applique un code promo
 * BUG CLASSIQUE #2 : Problème de coercition de type avec ==
 */
function applyCoupon(price, couponCode, validCoupons) {
    // Bug: Utiliser == au lieu de === peut causer des problèmes de coercition
    const coupon = validCoupons.find(c => c.code == couponCode);
    if (coupon) {
        return price - coupon.discount;
    }
    return price;
}

/**
 * Calcule le total du panier
 * BUG CONTEXTUEL : Pas de validation pour prix négatifs
 */
function calculateCartTotal(items) {
    let total = 0;
    items.forEach(item => {
        total += item.price * item.quantity;
    });
    // Bug: Validation manquante que le total ne devrait jamais être négatif
    return total;
}

/**
 * Formate le prix pour l'affichage
 * BUG CLASSIQUE #3 : toFixed retourne une string
 */
function formatPrice(price) {
    // Bug: toFixed retourne une string, peut causer des problèmes dans les calculs
    return price.toFixed(2) + ' EUR';
}

/**
 * Définit le prix d'un produit
 * BUG CONTEXTUEL : Pas de validation que le prix ne peut pas être négatif
 * Règle métier : Les prix e-commerce ne doivent jamais être négatifs
 */
function setProductPrice(product, newPrice) {
    // Bug: Règle métier manquante - les prix ne peuvent pas être négatifs
    product.price = newPrice;
    return product;
}

module.exports = {
    calculateDiscount,
    applyCoupon,
    calculateCartTotal,
    formatPrice,
    setProductPrice
};
