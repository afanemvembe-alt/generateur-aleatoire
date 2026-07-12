# Generateur de Mots de Passe Securises (Flask Web App)

Cette application Web developpee en Python avec Flask permet de generer des mots de passe aleatoires, hautement securises et faciles a retenir en y integrant des reperes personnels (fruit, animal ou date cle). L'algorithme se charge ensuite de combiner et melanger ces donnees avec des jeux de caracteres complexes (majuscules, chiffres, symboles).

## Fonctionnalites
* Interface Web Intuitive : Formulaire simple et epure pour configurer son mot de passe.
* Securisation Personnalisee : Mixage intelligent entre variables aleatoires et ancres mnemotechniques fournies par l'utilisateur.
* Longueur Ajustable : Controle total sur la taille finale du mot de passe genere.

## Installation et Lancement Local

1. Installer les dependances :
   ```bash
   pip install -r requirements.txt
   ```

2. Lancer l'application :
   ```bash
   python app.py
   ```
   L'application sera accessible sur votre navigateur a l'adresse http://127.0.0.1:5000.
