# � Guide simple pour la liaison Pronote

## C'est quoi ?

Le backend Python sert à récupérer tes vraies notes depuis Pronote automatiquement. C'est nécessaire car Pronote ne peut pas être connecté directement depuis une page web.

## Comment faire (3 étapes)

### Étape 1 : Installer sur ton ordinateur

Ouvre un terminal dans le dossier `backend` et tape :

```bash
pip install -r requirements.txt
```

### Étape 2 : Lancer le serveur

Toujours dans le dossier `backend` :

```bash
python app.py
```

Le serveur démarre et affiche : `Running on http://127.0.0.1:5000`

### Étape 3 : Utiliser sur l'app

1. Ouvre l'application web sur ton navigateur
2. Clique sur "Récupérer depuis Pronote"
3. Entre ton URL Pronote, nom d'utilisateur et mot de passe
4. Ta vraie moyenne apparaît automatiquement !

## Pour l'utiliser sur iPhone (en ligne)

Pour que ça marche sur ton iPhone, il faut déployer le backend en ligne (gratuit) :

### Option la plus simple : Render

1. Va sur https://render.com et crée un compte
2. Clique sur "New" → "Web Service"
3. Connecte ton compte GitHub
4. Crée un repository avec le dossier `backend`
5. Configure :
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `python app.py`
6. Clique sur "Deploy"
7. Copie l'URL donnée (ex: https://brevet-pro.onrender.com)
8. Dans `index.html`, remplace `http://localhost:5000` par cette URL

## Alternative plus simple

Si tu veux éviter tout ça, utilise l'application Python originale (`main.py`) sur ton ordinateur. Elle a déjà la liaison Pronote complète et sécurisée !
