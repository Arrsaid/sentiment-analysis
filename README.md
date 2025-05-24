# Prédiction de sentiment sur Twitter – Projet Air Paradis

## Objectif du projet
Ce projet a été réalisé dans le cadre d’une mission chez MIC (Marketing Intelligence Consulting) pour le client Air Paradis. L’objectif est de développer un prototype d’intelligence artificielle capable de prédire le sentiment (positif ou négatif) d’un tweet, afin d’anticiper les bad buzz sur les réseaux sociaux.

## Contenu du projet
Le projet est organisé comme suit :

### 1. Notebooks de modélisation
- `Modelisation_part_1.ipynb` : nettoyage des données, prétraitement, modélisation classique (régression logistique) + LSTM et suivi avec MLFlow.
- `Modelisation_part_2.ipynb` : modélisation avancée BERT et suivi avec MLFlow.

### 2. Scripts Python
- `api.py` : API développée avec FastAPI pour exposer le modèle avancé.
- `app.py` : application Streamlit pour tester l’API en local.
- `test_api.py` : script de tests unitaires pour vérifier le bon fonctionnement de l’API.
- `utils.py` : script contient des fonctions de prétraitemet utiliser dans les notebooks et dans le fichier api.py.

### 3. Fichiers de configuration
- `requirements.txt` : liste des packages nécessaires pour le developement et le deploiment de l'api.
- `requirements_mod.txt` : liste des packages nécessaires pour la modelisation.
- `.github/workflows/deploy.yml` : pipeline GitHub Actions pour le déploiement continu sur Azure Web App.

## Déploiement
Le modèle classique (régression logistique) a été déployé sur Azure Web App (plan gratuit) avec un pipeline CI/CD via GitHub Actions. 

## Interface utilisateur
Une interface Streamlit permet de tester l’API localement. L’utilisateur saisit un tweet, visualise la prédiction et peut la valider ou la rejeter.

## Suivi en production
Azure Application Insights est utilisé pour :
- remonter les tweets mal prédits (texte et prédiction),
- déclencher une alerte si trois erreurs surviennent en moins de cinq minutes.

## Remarques
Les répertoires générés automatiquement par MLFlow (`mlruns`, `artifacts`, etc.) ne sont pas inclus dans le livrable. Le projet intègre également une démarche MLOps complète (tracking, déploiement, monitoring).

---


