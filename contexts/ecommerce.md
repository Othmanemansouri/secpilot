# Contexte Client : E-Commerce

## Domaine métier
Plateforme de vente en ligne de produits grand public.

## Règles métier critiques

### Règle EC-001 : Prix non-négatif
**Priorité** : CRITIQUE
**Description** : Les prix des produits ne doivent JAMAIS être négatifs.

**Justification** :
- Un prix négatif signifierait payer le client pour prendre un produit
- Risque de fraude financière
- Violation des principes fondamentaux du e-commerce

**Exigences de validation** :
- Toutes les fonctions de modification de prix doivent valider que l'entrée >= 0
- Les calculs de remise doivent plafonner à 100% (résultat = 0.00€)
- Toute fonction retournant un prix doit garantir une sortie non-négative

**Scénarios de test** :
1. Définir un prix à -10 → doit lever une erreur ValidationError
2. Remise de 150% → doit résulter en 0.00€, pas en négatif
3. Les remises groupées ne doivent jamais dépasser le total des articles

### Règle EC-002 : Limites de remise
**Priorité** : HAUTE
**Description** : Les remises ne peuvent pas dépasser 100% du prix original.

**Exigences de validation** :
- Le pourcentage de remise doit être entre 0 et 100
- Prix final = max(0, original - remise)

### Règle EC-003 : Précision monétaire
**Priorité** : MOYENNE
**Description** : Tous les calculs monétaires doivent maintenir une précision à 2 décimales.

**Exigences de validation** :
- Utiliser des types décimaux appropriés (pas de virgule flottante)
- Arrondir de manière cohérente (arrondi bancaire recommandé)

## Terminologie du domaine
- **SKU** : Stock Keeping Unit - identifiant unique de produit
- **Panier** : Collection temporaire d'articles pour achat
- **Checkout** : Processus de finalisation d'un achat

## Fichiers de code associés
- `src/*/ecommerce/pricing.*`

## Exigences de couverture de tests
- Tests unitaires pour tous les calculs de prix
- Cas limites : prix à zéro, remises maximales, seuils de volume
