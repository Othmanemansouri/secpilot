/**
 * Module de virement bancaire
 * Contexte client : Système bancaire où les virements doivent être refusés si solde insuffisant
 */

/**
 * Transfère des fonds entre comptes
 * BUG CONTEXTUEL : Ne vérifie pas le solde avant le virement
 * Règle métier : Refuser le virement si l'émetteur a un solde insuffisant
 */
function transferFunds(fromAccount, toAccount, amount) {
    // Bug: Validation du solde manquante
    fromAccount.balance -= amount;
    toAccount.balance += amount;
    return { success: true, message: 'Virement effectué' };
}

/**
 * Valide un numéro de compte
 * BUG CLASSIQUE #1 : Vulnérabilité ReDoS dans la regex
 */
function validateAccountNumber(accountNumber) {
    // Bug: Backtracking catastrophique possible avec une entrée malveillante
    const pattern = /^(\d+)+$/;
    return pattern.test(accountNumber);
}

/**
 * Calcule la mensualité d'un prêt
 * BUG CLASSIQUE #2 : Propagation de NaN
 */
function calculateMonthlyPayment(principal, annualRate, months) {
    // Bug: Division par zéro quand annualRate est 0
    const monthlyRate = annualRate / 12;
    const payment = principal * (monthlyRate * Math.pow(1 + monthlyRate, months))
                    / (Math.pow(1 + monthlyRate, months) - 1);
    return payment;  // Retourne NaN quand rate est 0
}

/**
 * Vérifie si une transaction est suspecte
 * BUG CLASSIQUE #3 : Problème de comparaison d'objets
 */
function isTransactionSuspicious(transaction, suspiciousPatterns) {
    // Bug: Compare les références, pas les valeurs
    return suspiciousPatterns.includes(transaction.pattern);
}

/**
 * Obtient le solde d'un compte
 * BUG CLASSIQUE #4 : Gestion des comptes inexistants
 */
function getAccountBalance(accountId, accounts) {
    // Bug: Devrait gérer le cas où le compte n'existe pas
    return accounts[accountId].balance;
}

module.exports = {
    transferFunds,
    validateAccountNumber,
    calculateMonthlyPayment,
    isTransactionSuspicious,
    getAccountBalance
};
