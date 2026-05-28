import streamlit as st
import pandas as pd
import plotly.express as px


def format_prix(valeur):
    return f"{int(valeur):,} €".replace(',', ' ')


def format_km(valeur):
    return f"{int(valeur):,} km".replace(',', ' ')


# 1. Configuration
st.set_page_config(page_title="RIDE Dashboard", layout="wide")

# 2. Chargement et NETTOYAGE
@st.cache_data
def load_data():
    df = pd.read_csv("CAR DETAILS FROM CAR DEKHO.csv")
    df = df.drop_duplicates() # Supprime les doublons
    df['name'] = df['name'].str.strip()
    df['brand'] = df['name'].str.split(' ').str[0]
    return df

df = load_data()

# 3. BARRE LATÉRALE
st.sidebar.header("⚙️ Configuration")
marques = sorted(df['brand'].unique())
marque_choisie = st.sidebar.selectbox("Quelle marque ?", marques)

prix_max_possible = int(df['selling_price'].max())
budget_defaut = min(500000, prix_max_possible)
budget = st.sidebar.slider(
    "Budget max (€)",
    0,
    prix_max_possible,
    budget_defaut,
    step=10000,
    format="%d €"
)
st.sidebar.caption(f"Budget sélectionné : {format_prix(budget)}")

annee_min = st.sidebar.slider(
    "Année minimum",
    int(df['year'].min()),
    int(df['year'].max()),
    int(df['year'].min())
)

km_max_possible = int(df['km_driven'].max())
km_max = st.sidebar.slider(
    "Kilométrage maximum",
    0,
    km_max_possible,
    km_max_possible,
    step=10000,
    format="%d km"
)
st.sidebar.caption(f"Kilométrage sélectionné : {format_km(km_max)}")

# Filtrage principal
df_filtre = df[
    (df['brand'] == marque_choisie) &
    (df['selling_price'] <= budget) &
    (df['year'] >= annee_min) &
    (df['km_driven'] <= km_max)
]

carburants_disponibles = ["Tous"] + sorted(df_filtre['fuel'].unique())
carburant_choisi = st.sidebar.selectbox("Type de carburant", carburants_disponibles)

if carburant_choisi != "Tous":
    df_filtre = df_filtre[df_filtre['fuel'] == carburant_choisi]


def normaliser_score(serie, inverser=False):
    minimum = serie.min()
    maximum = serie.max()

    if minimum == maximum:
        return pd.Series(1, index=serie.index)

    score = (serie - minimum) / (maximum - minimum)

    if inverser:
        score = 1 - score

    return score


if not df_filtre.empty:
    df_recommandation = df_filtre.copy()
    df_recommandation['score_prix'] = normaliser_score(df_recommandation['selling_price'], inverser=True)
    df_recommandation['score_km'] = normaliser_score(df_recommandation['km_driven'], inverser=True)
    df_recommandation['score_annee'] = normaliser_score(df_recommandation['year'])
    df_recommandation['score_recommandation'] = (
        df_recommandation['score_prix'] * 0.4 +
        df_recommandation['score_km'] * 0.3 +
        df_recommandation['score_annee'] * 0.3
    )
    df_recommandation['score_recommandation_pct'] = df_recommandation['score_recommandation'] * 100
    top_recommandations = df_recommandation.sort_values('score_recommandation', ascending=False).head(5)
else:
    top_recommandations = pd.DataFrame()

# 4. AFFICHAGE
st.title("🚗 RIDE : Analyse du marché automobile d'occasion")

st.markdown("""
Ce dashboard interactif analyse un dataset de voitures d'occasion afin d'étudier les prix
selon la marque, l'année, le kilométrage et le type de carburant.

**Objectif :** mieux comprendre les facteurs qui influencent le prix de vente d'un véhicule
et proposer une lecture simple des tendances du marché.
""")

if df_filtre.empty:
    nb_voitures = 0
    prix_moyen = "-"
    prix_min = "-"
    prix_max = "-"
    km_moyen = "-"
    annee_moyenne = "-"
    st.warning("Aucun véhicule trouvé avec ces filtres. Modifie la marque, le budget, l'année ou le kilométrage.")
else:
    nb_voitures = len(df_filtre)
    prix_moyen = format_prix(df_filtre['selling_price'].mean())
    prix_min = format_prix(df_filtre['selling_price'].min())
    prix_max = format_prix(df_filtre['selling_price'].max())
    km_moyen = format_km(df_filtre['km_driven'].mean())
    annee_moyenne = int(df_filtre['year'].mean())

col1, col2, col3 = st.columns(3)
col1.metric("Véhicules trouvés", nb_voitures)
col2.metric("Prix moyen", prix_moyen)
col3.metric("KM moyen", km_moyen)

col4, col5, col6 = st.columns(3)
col4.metric("Prix minimum", prix_min)
col5.metric("Prix maximum", prix_max)
col6.metric("Année moyenne", annee_moyenne)

st.divider()

# 5. ANALYSE RAPIDE
st.write("### 📌 Analyse rapide")

if df_filtre.empty:
    st.info("Aucune analyse disponible pour ces filtres, car aucun véhicule ne correspond à la recherche.")
else:
    vehicule_recommande = top_recommandations.iloc[0]
    carburant_analyse = carburant_choisi if carburant_choisi != "Tous" else "tous carburants"

    st.markdown(f"""
    Pour la marque **{marque_choisie}**, avec un budget maximum de **{budget:,} €**,
    le dashboard trouve **{nb_voitures} véhicule(s)** correspondant aux filtres.

    Le prix moyen est de **{prix_moyen}** et le kilométrage moyen est de **{km_moyen}**.
    Le meilleur véhicule recommandé par le score est **{vehicule_recommande['name']}**,
    car il combine un prix compétitif, un kilométrage faible et une année récente.

    Filtres appliqués : **{carburant_analyse}**, année minimum **{annee_min}**,
    kilométrage maximum **{km_max:,} km**.
    """.replace(',', ' '))

st.divider()

# 6. RECOMMANDATIONS
st.write("### ⭐ Top recommandations")

if top_recommandations.empty:
    st.info("Les recommandations apparaîtront quand au moins un véhicule correspondra aux filtres.")
else:
    st.caption("Score calculé selon le prix, le kilométrage et l'année du véhicule.")
    st.dataframe(
        top_recommandations[['name', 'year', 'selling_price', 'km_driven', 'fuel', 'score_recommandation_pct']],
        column_config={
            "name": "Véhicule",
            "year": st.column_config.NumberColumn("Année", format="%d"),
            "selling_price": st.column_config.NumberColumn("Prix", format="%d €"),
            "km_driven": st.column_config.NumberColumn("KM", format="%d km"),
            "fuel": "Carburant",
            "score_recommandation_pct": st.column_config.ProgressColumn(
                "Score",
                format="%.0f %%",
                min_value=0,
                max_value=100
            )
        },
        hide_index=True,
        width="stretch"
    )

st.divider()

# 7. VISUALISATIONS
st.write("### 📊 Prix moyen par type de carburant")

if df_filtre.empty:
    st.info("Le graphique apparaîtra quand au moins un véhicule correspondra aux filtres.")
else:
    prix_carburant = (
        df_filtre.groupby('fuel', as_index=False)['selling_price']
        .mean()
        .sort_values('selling_price', ascending=False)
    )
    prix_carburant['prix_moyen_label'] = prix_carburant['selling_price'].apply(format_prix)

    fig_carburant = px.bar(
        prix_carburant,
        x="fuel",
        y="selling_price",
        text="prix_moyen_label",
        template="plotly_white",
        labels={
            "fuel": "Carburant",
            "selling_price": "Prix moyen (€)"
        }
    )
    fig_carburant.update_traces(textposition="outside")
    fig_carburant.update_yaxes(tickformat=",")
    st.plotly_chart(fig_carburant, width="stretch")

st.divider()

# 8. RELATION PRIX / KILOMÉTRAGE
st.write("### 📉 Prix selon le kilométrage")

if df_filtre.empty:
    st.info("Le graphique apparaîtra quand au moins un véhicule correspondra aux filtres.")
else:
    fig_km = px.scatter(
        df_filtre,
        x="km_driven",
        y="selling_price",
        color="fuel",
        hover_name="name",
        template="plotly_white",
        labels={
            "km_driven": "Kilométrage",
            "selling_price": "Prix (€)",
            "fuel": "Carburant"
        }
    )
    st.plotly_chart(fig_km, width="stretch")

st.divider()

# 9. GRAPHIQUE ET TABLEAU
col_g, col_d = st.columns([1, 1])

with col_g:
    st.write("### 📈 Rapport Prix / Année")
    if df_filtre.empty:
        st.info("Le graphique apparaîtra quand au moins un véhicule correspondra aux filtres.")
    else:
        fig = px.scatter(df_filtre, x="year", y="selling_price", color="fuel", 
                         hover_name="name", template="plotly_white")
        st.plotly_chart(fig, width="stretch")

with col_d:
    st.write("### 📄 Liste des véhicules")
    if df_filtre.empty:
        st.info("La liste apparaîtra quand au moins un véhicule correspondra aux filtres.")
    else:
        st.dataframe(
            df_filtre[['name', 'year', 'selling_price', 'km_driven']], 
            column_config={
                "selling_price": st.column_config.NumberColumn("Prix", format="%d €"),
                "km_driven": st.column_config.NumberColumn("KM", format="%d km"),
                "year": st.column_config.NumberColumn("Année", format="%d")
            },
            width="stretch"
        )

