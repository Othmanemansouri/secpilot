# Contexte Client : Santé

## Domaine métier
Système de calcul de dosages médicamenteux pour professionnels de santé.

## Règles métier critiques

### Règle HC-001 : Application de la dose maximale
**Priorité** : CRITIQUE - SÉCURITÉ PATIENT
**Description** : Les dosages de médicaments ne doivent JAMAIS dépasser les limites maximales sûres.

**Justification** :
- La sécurité du patient est primordiale
- Les surdosages peuvent causer des dommages graves ou la mort
- Exigence réglementaire (ANSM, FDA, etc.)

**Doses maximales sûres (journalières)** :
| Médicament     | Dose max (mg) | Notes                        |
|----------------|---------------|------------------------------|
| Paracétamol    | 4000          | Risque de toxicité hépatique |
| Ibuprofène     | 3200          | Risque de saignement GI      |
| Aspirine       | 4000          | Risque hémorragique          |

**Exigences de validation** :
- TOUJOURS plafonner la dose calculée à la limite maximale sûre
- Journaliser des avertissements quand la dose dépasserait le maximum
- Retourner la dose plafonnée, pas la dose calculée

**Scénarios de test** :
1. Patient 150kg à 30mg/kg = 4500mg → doit retourner 4000mg (plafonné)
2. Patient 50kg à 30mg/kg = 1500mg → doit retourner 1500mg (dans la limite)
3. Médicament inconnu → doit lever une erreur ou utiliser une valeur par défaut prudente

### Règle HC-002 : Vérification des interactions médicamenteuses
**Priorité** : CRITIQUE - SÉCURITÉ PATIENT
**Description** : Les combinaisons de médicaments dangereuses doivent être signalées.

**Combinaisons dangereuses connues** :
- Warfarine + Aspirine (risque hémorragique)
- Metformine + Alcool (acidose lactique)

**Exigences de validation** :
- Correspondance des noms de médicaments insensible à la casse
- Vérifier les deux ordres (A+B et B+A)

### Règle HC-003 : Sécurité de la fréquence de dose
**Priorité** : HAUTE
**Description** : Le fractionnement des doses doit gérer les cas limites en toute sécurité.

**Exigences de validation** :
- La fréquence ne peut pas être zéro (division par zéro)
- Fréquence minimum de 1 dose par jour

## Terminologie du domaine
- **Dose** : Quantité de médicament administrée en une fois
- **Fréquence** : Nombre de prises par jour
- **Contre-indication** : Raison de ne pas administrer un traitement

## Fichiers de code associés
- `src/*/healthcare/dosage.*`

## Conformité réglementaire
- Directives ANSM pour les calculs de dosage
- Normes de sécurité médicamenteuse
