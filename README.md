# Web Scraping Blog du Modérateur

Ce projet permet de scraper les articles du Blog du Modérateur et de les stocker dans une base MongoDB, avec une interface web pour effectuer des recherches avancées.

## Fonctionnalités

### Partie 1 : Scraping (TP_1.py)

- Récupération des articles depuis le Blog du Modérateur
- Extraction des informations :
  - URL
  - Titre
  - Catégorie
  - Date de publication
  - Sous-catégorie
  - Résumé
  - Contenu
  - Images
  - Auteur
  - Image miniature
- Stockage dans MongoDB

### Partie 2 : Interface Web (app.py)

- Interface de recherche avec les critères suivants :
  - Date de publication (début/fin)
  - Auteur
  - Catégorie
  - Sous-catégorie
  - Recherche dans le titre
- Affichage des résultats avec :
  - Image miniature
  - Informations détaillées
  - Lien vers l'article original

## Prérequis

- Python 3.8+
- MongoDB
- Packages Python :
  - requests
  - beautifulsoup4
  - pymongo
  - flask

## Installation

1. Cloner le repository :

```bash
git clone [URL_DU_REPO]
cd [NOM_DU_DOSSIER]
```

2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

3. S'assurer que MongoDB est en cours d'exécution

## Structure du Projet

```
projet/
    ├── TP_1.py           # Script de scraping
    ├── app.py            # Application Flask
    ├── requirements.txt  # Dépendances
    ├── README.md        # Documentation
    └── templates/
        └── index.html   # Template de l'interface web
```

## Utilisation

### 1. Scraping des Articles

Pour récupérer les articles :

```bash
python TP_1.py
```

### 2. Interface Web

Pour lancer l'interface de recherche :

```bash
python app.py
```

Puis accéder à l'interface dans votre navigateur :

```
http://localhost:5000
```

## Fonctionnalités de Recherche

1. **Recherche par Date**

   - Sélectionnez une période avec date de début et de fin

2. **Recherche par Auteur**

   - Sélectionnez un auteur dans la liste déroulante

3. **Recherche par Catégorie**

   - Filtrez par catégorie principale

4. **Recherche par Sous-catégorie**

   - Filtrez par sous-catégorie

5. **Recherche dans le Titre**
   - Entrez un mot-clé pour rechercher dans les titres

## Base de Données

Les articles sont stockés dans MongoDB avec la structure suivante :

```json
{
  "url": "URL de l'article",
  "title": "Titre de l'article",
  "category": "Catégorie principale",
  "date": "Date de publication",
  "subcategory": "Sous-catégorie",
  "summary": "Résumé de l'article",
  "images": {
    "url_image": "légende"
  },
  "author": "Nom de l'auteur",
  "thumbnail": "URL de l'image miniature"
}