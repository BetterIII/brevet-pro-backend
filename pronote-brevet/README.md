# Brevet Pro - Calculateur et Simulateur d'Examen

Application Python pour calculer et simuler le brevet des collèges avec intégration Pronote.

## 🎯 Fonctionnalités

- **Calculateur de brevet** : Calcule votre moyenne finale selon les coefficients officiels (40% contrôle continu, 60% épreuves)
- **Intégration Pronote** : Connectez votre compte Pronote pour récupérer automatiquement votre moyenne de contrôle continu
- **Simulateur de brevet blanc** : Entraînez-vous avec des sujets types des sessions précédentes (7 matières)
- **Thèmes** : Interface en mode sombre ou clair
- **Calcul rapide** : Estimez votre note finale rapidement

## 📋 Prérequis

- Python 3.8 ou supérieur
- Windows (recommandé)

## 🚀 Installation

1. Clonez ou téléchargez ce dossier
2. Double-cliquez sur `lancer.bat` pour installer les dépendances et lancer l'application

Ou manuellement :

```bash
pip install -r requirements.txt
python main.py
```

## 🔗 Connexion Pronote

Pour lier votre compte Pronote :

1. Ouvrez l'application Pronote sur votre téléphone
2. Allez dans Menu → QR code → Afficher mon QR code
3. Notez le code PIN à 4 chiffres
4. Dans Brevet Pro, cliquez sur "LIER MON COMPTE PRONOTE"
5. Entrez le PIN et importez la capture du QR code (ou collez le texte du QR code)

## 📚 Matières du brevet blanc

- Français
- Mathématiques
- Histoire
- Géographie
- EMC (Enseignement Moral et Civique)
- Physique-Chimie
- SVT (Sciences de la Vie et de la Terre)

## 🎮 Utilisation

### Calcul rapide
1. Allez dans l'onglet "Calcul rapide"
2. Entrez votre note d'épreuves sur 20
3. Cliquez sur "CALCULER"
4. Le résultat s'affiche avec votre mention potentielle

### Brevet blanc
1. Allez dans l'onglet "Brevet blanc"
2. Cliquez sur "COMMENCER LE BREVET BLANC"
3. Répondez aux questions QCM pour chaque matière
4. Pas de retour en arrière possible
5. Vos résultats s'affichent à la fin avec la mention

### Paramètres
- Changez le thème (sombre/clair)
- Entrez manuellement votre moyenne de contrôle continu si Pronote n'est pas lié
- Déconnectez votre compte Pronote

## 📊 Calcul du brevet

- **Contrôle continu** : 40% de la note finale (moyenne annuelle)
- **Épreuves** : 60% de la note finale (moyenne des 7 matières)

### Mentions
- **Très bien avec félicitations** : 18/20 et plus
- **Très bien** : 16/20 à 17.99/20
- **Bien** : 14/20 à 15.99/20
- **Assez bien** : 12/20 à 13.99/20
- **Admis sans mention** : 10/20 à 11.99/20

## 🔒 Sécurité

- Vos identifiants Pronote sont stockés localement dans `credentials.json`
- Le code PIN Pronote n'est jamais sauvegardé
- L'application utilise l'API officielle pronotepy

## 🐛 Problèmes courants

**"Session expirée"** : Reliez votre compte Pronote à nouveau

**"Aucune note trouvée"** : Vérifiez que vous avez des notes sur Pronote pour la période en cours

**Erreur de dépendances** : Lancez `lancer.bat` pour réinstaller les dépendances

## 📝 Fichiers

- `main.py` : Application principale
- `examens.py` : Banque de sujets type brevet
- `config.json` : Configuration (ne pas modifier)
- `credentials.json` : Identifiants Pronote chiffrés
- `settings.json` : Préférences utilisateur (créé automatiquement)
- `requirements.txt` : Dépendances Python

## 📄 Licence

Ce projet est à usage éducatif personnel.

---

**Bon courage pour votre brevet ! 🎓**
