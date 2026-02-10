# Contexte Client : Banque

## Domaine métier
Plateforme bancaire numérique pour comptes particuliers et professionnels.

## Règles métier critiques

### Règle BK-001 : Prévention du découvert
**Priorité** : CRITIQUE
**Description** : Les virements doivent être REFUSÉS si le solde de l'émetteur est insuffisant.

**Justification** :
- Prévient les découverts non autorisés
- Maintient l'intégrité des comptes
- Exigence réglementaire bancaire

**Exigences de validation** :
- Vérifier le solde AVANT d'initier le virement
- La vérification du solde doit être atomique avec le virement
- Retourner une erreur claire en cas de fonds insuffisants

**Scénarios de test** :
1. Virement de 100€ avec solde de 50€ → doit échouer
2. Virement de 100€ avec solde de 100€ → doit réussir
3. Virement de 100.01€ avec solde de 100€ → doit échouer

### Règle BK-002 : Validation du numéro de compte
**Priorité** : HAUTE
**Description** : Les numéros de compte doivent contenir exactement 10 chiffres.

**Exigences de validation** :
- Exactement 10 caractères numériques
- Pas de lettres ni de caractères spéciaux
- Les zéros en tête sont significatifs

### Règle BK-003 : Précision financière
**Priorité** : CRITIQUE
**Description** : Tous les calculs monétaires doivent utiliser des décimaux à précision arbitraire.

**Exigences de validation** :
- Ne jamais utiliser float/double pour l'argent
- Utiliser BigDecimal (Java), Decimal (Python), ou équivalent
- Minimum 4 décimales pour les calculs intermédiaires

## Terminologie du domaine
- **Principal** : Montant initial dans un prêt ou investissement
- **TAEG** : Taux Annuel Effectif Global
- **Virement** : Transfert de fonds entre comptes

## Fichiers de code associés
- `src/*/banking/transfer.*`

## Conformité réglementaire
- Doit respecter les réglementations bancaires sur la protection contre les découverts
- Piste d'audit requise pour toutes les transactions
