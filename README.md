# RIDE - Dashboard d'analyse de voitures d'occasion

RIDE est un dashboard interactif développé avec Streamlit pour analyser un dataset de voitures d'occasion.

L'objectif du projet est d'aider un utilisateur à explorer le marché automobile selon plusieurs critères : marque, budget, année, kilométrage et type de carburant.

## Objectifs du projet

- Nettoyer et préparer un dataset automobile.
- Créer des filtres interactifs pour explorer les données.
- Afficher des indicateurs clés pour faciliter l'analyse.
- Visualiser les tendances du marché automobile d'occasion.
- Proposer un premier système de recommandation basé sur un score simple.

## Fonctionnalités

- Filtrage par marque.
- Filtrage par budget maximum.
- Filtrage par année minimum.
- Filtrage par kilométrage maximum.
- Filtrage dynamique par type de carburant.
- KPIs : véhicules trouvés, prix moyen, kilométrage moyen, prix minimum, prix maximum, année moyenne.
- Top recommandations selon un score basé sur le prix, le kilométrage et l'année.
- Analyse rapide générée automatiquement selon les filtres.
- Graphiques interactifs avec Plotly.
- Tableau détaillé des véhicules filtrés.

## Système de recommandation

Le dashboard calcule un score de recommandation pour chaque véhicule filtré.

Le score prend en compte :

- 40 % : prix du véhicule, avec un meilleur score pour les prix les plus bas.
- 30 % : kilométrage, avec un meilleur score pour les véhicules les moins kilométrés.
- 30 % : année, avec un meilleur score pour les véhicules les plus récents.

Ce système n'est pas encore une intelligence artificielle avancée, mais il représente une première logique de recommandation métier.

## Technologies utilisées

- Python
- Pandas
- Streamlit
- Plotly Express

## Structure du projet

```text
projet3/
├── app.py
├── CAR DETAILS FROM CAR DEKHO.csv
├── car data.csv
├── Car details v3.csv
├── car details v4.csv
└── README.md
```

## Lancer le projet

Installer les dépendances :

```bash
pip install streamlit pandas plotly
```

Lancer l'application :

```bash
streamlit run app.py
```

Si la commande `streamlit` n'est pas reconnue :

```bash
python -m streamlit run app.py
```

## Compétences démontrées

- Chargement et nettoyage de données avec Pandas.
- Création d'une colonne métier à partir d'une donnée existante.
- Construction d'un dashboard interactif.
- Création de filtres utilisateur.
- Calcul d'indicateurs de performance.
- Visualisation de données avec Plotly.
- Mise en place d'une logique de scoring simple.
- Présentation d'une analyse compréhensible pour un utilisateur non technique.

## Améliorations possibles

- Ajouter une option "Toutes les marques".
- Ajouter un modèle de prédiction du prix d'un véhicule.
- Ajouter une comparaison entre plusieurs marques.
- Déployer l'application sur Streamlit Community Cloud.
- Ajouter des captures d'écran du dashboard dans ce README.
