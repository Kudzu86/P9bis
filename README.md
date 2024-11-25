# **Application de critiques de livres et articles**

## **Résumé du projet**
Cette application permet aux utilisateurs :
- **De publier des critiques** de livres, d'articles, etc.
- **De demander des critiques** en créant des billets.
- **De répondre aux demandes de critiques** des autres utilisateurs.
- **De consulter des critiques** publiées par d'autres utilisateurs.
- **De suivre et de gérer les utilisateurs suivis** pour personnaliser son flux d'activités.

L'objectif est de créer une communauté où les utilisateurs peuvent échanger des avis et critiques littéraires de manière collaborative.
Cette application offre une expérience simple et accessible, conforme aux directives **WCAG**, pour consulter et partager des avis littéraires.

---

## **Fonctionnalités**

### **Pour les visiteurs**
- S'inscrire pour créer un compte.
- Se connecter pour accéder à leur flux personnalisé.

### **Pour les utilisateurs connectés**
#### **Flux personnalisé :**
- Affiche les billets et critiques des utilisateurs suivis.
- Peut inclure leurs propres publications.
- Classe les contenus par ordre antéchronologique (les plus récents en premier).

#### **Billets :**
- Créer des billets pour demander des critiques sur un livre ou un article.
- Modifier ou supprimer leurs billets.
- Combiner la création d'un billet et d'une critique en une seule étape.

#### **Critiques :**
- Répondre aux billets d'autres utilisateurs.
- Créer des critiques indépendantes directement.
- Modifier ou supprimer leurs critiques.

#### **Suivi des utilisateurs :**
- Rechercher et suivre des utilisateurs.
- Voir la liste des utilisateurs suivis.
- Ne plus suivre des utilisateurs.

---

## **Installation et configuration**

### **Prérequis**
- **Python** (version 3.9 ou supérieure)
- **Django** (version 4.0 ou supérieure)
- **SQLite** (inclus avec Django)
- Un environnement virtuel Python est recommandé.

### **Étapes d'installation**

1. **Cloner le repository GitHub** :
   ```
   git clone https://github.com/Kudzu86/P9bis/tree/master
   cd mon_projet
   ```

2. **Créer et activer un environnement virtuel** :
   ```
   python -m venv env
   source env/bin/activate  # Sur Windows, utilisez env\Scripts\activate
   ```

3. **Installer les dépendances** :
   ```
   pip install -r requirements.txt
   ```

4. **Appliquer les migrations de basede données** :
   ```
   python manage.py migrate
   ```

5. **Créer un utilisateur administrateur (optionnel)** :
   ```
   python manage.py createsuperuser
   ```

6. **Lancer le serveur local** :
   ```
   python manage.py runserver
   ```

7. **Accéder à l'application : Ouvrez http://127.0.0.1:8000 dans votre navigateur**.

---

## **Structure du projet**

### **Principaux fichiers et répertoires**
- `manage.py` : Commande d'administration principale de Django.
- `review/` : Répertoire principal contenant le code source de l'application.
  - `models.py` : Définition des modèles de données.
  - `views.py` : Logique métier pour chaque page.
  - `forms.py` : Définition des formulaires personnalisés.
  - `templates/` : Fichiers HTML pour les pages du site.
   
---

## **Schéma de base de données**

Le schéma de base de données comprend les principales entités suivantes :
- **Utilisateur (CustomUser)** :
  - `username`, `email`, `birth_date`, `gender`
- **Billet (Ticket)** :
  - `title`, `description`, `user`, `time_created`
- **Critique (Review)** :
  - `headline`, `body`, `rating`, `ticket`, `user`, `time_created`
- **Utilisateur Suivi (UserFollows)** :
  - `user`, `followed_user`

---
   
## **Tests et données de démonstration**

- L'application inclut des données de test pour faciliter la démonstration.
- Inclut un fichier db.sqlite3 prérempli.
- Compte administrateur de test :
  - **Nom d'utilisateur :** `Kudzu`
  - **Mot de passe :** `jose`

---

## **Contributeurs**

- Développeur : Auer Eric


