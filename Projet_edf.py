import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- Configuration de la page ---
st.set_page_config(
    page_title="Analyse des Matchs de l'Équipe de France",
    page_icon="🇫🇷",
    layout="wide"
)

# --- Charger et nettoyer les données ---
@st.cache_data
def load_data():
    df = pd.read_csv('df_matches.csv', sep=';', quotechar='"', encoding='utf-8')
    # Supprimer les colonnes inutiles
    df = df.drop(columns=['X2', 'X5', 'no'], errors='ignore')
    # Traduire "outcome" en français
    df['Résultat'] = df['outcome'].map({'win': 'Victoire', 'loss': 'Défaite', 'draw': 'Nul'})
    # Convertir la date et extraire l'année
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['Année'] = df['date'].dt.year
    return df

df = load_data()

# --- Barre latérale pour la décennie ---
with st.sidebar:
    st.header("🎛️ Filtres")
    decade = st.slider(
        "Décennie",
        min_value=1900,
        max_value=2020,
        value=(1950, 2020),
        step=10
    )

# --- Filtrer les données par décennie ---
df_filtered = df[(df['year'] >= decade[0]) & (df['year'] <= decade[1])]

# --- Titre et description ---
st.title("🇫🇷 Analyse et Simulation des Matchs de l'Équipe de France")
st.markdown(f"""
Cette application permet d'explorer les **statistiques historiques** de l'équipe de France ({len(df_filtered)} matchs entre {decade[0]} et {decade[1]}).
""")

# --- Section 1 : Tableau de bord général ---
st.header("📊 Tableau de bord")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Matchs joués", len(df_filtered))
col2.metric("Victoires", (df_filtered['outcome'] == 'win').sum())
col3.metric("Défaites", (df_filtered['outcome'] == 'loss').sum())
col4.metric("Nuls", (df_filtered['outcome'] == 'draw').sum())

# Graphique : Évolution des buts par décennie
df_filtered['Décennie'] = (df_filtered['year'] // 10) * 10
buts_par_décennie = df_filtered.groupby('Décennie').agg({
    'score_france': 'mean',
    'score_adversaire': 'mean'
}).reset_index()

fig_buts = px.line(
    buts_par_décennie,
    x='Décennie',
    y=['score_france', 'score_adversaire'],
    title=f"Moyenne de buts marqués/concédés par décennie ({decade[0]}-{decade[1]})",
    labels={'value': 'Nombre de buts', 'variable': 'Type de buts'},
    color_discrete_sequence=['#0055A4', '#EF4135']  # Couleurs de l'équipe de France
)
st.plotly_chart(fig_buts, use_container_width=True)

# Camembert : Répartition des résultats
fig_pie = px.pie(
    df_filtered,
    names='Résultat',
    title=f"Répartition des résultats ({decade[0]}-{decade[1]})",
    color_discrete_sequence=px.colors.qualitative.Set3,
    hole=0.3
)
st.plotly_chart(fig_pie, use_container_width=True)

# --- Section 2 : Simulation de match ---
st.header("🎮 Simulation de match")

# Liste des adversaires disponibles (filtrés par décennie)
adversaires = df_filtered['adversaire'].unique()
if len(adversaires) == 0:
    st.error(f"Aucun adversaire trouvé entre {decade[0]} et {decade[1]}. Elargis la période.")
    st.stop()

adversaire = st.selectbox("Choisir un adversaire", adversaires)

# Filtrer les matchs contre cet adversaire (avec la décennie appliquée)
matches_adversaire = df_filtered[df_filtered['adversaire'] == adversaire]

st.subheader(f"📊 Bilan contre {adversaire} ({decade[0]}-{decade[1]})")
col1, col2, col3 = st.columns(3)
col1.metric("Victoires", (matches_adversaire['outcome'] == 'win').sum())
col2.metric("Défaites", (matches_adversaire['outcome'] == 'loss').sum())
col3.metric("Nuls", (matches_adversaire['outcome'] == 'draw').sum())


# --- Derniers matchs ---
st.subheader(f"📜 Derniers matchs contre {adversaire} ({decade[0]}-{decade[1]})")
if len(matches_adversaire) > 0:
    st.dataframe(
        matches_adversaire.sort_values('year', ascending=False)[
            ['date', 'score_france', 'score_adversaire', 'Résultat']
        ].head(5),
        hide_index=True,
        use_container_width=True
    )
else:
    st.info(f"Aucun match historique disponible contre {adversaire} entre {decade[0]} et {decade[1]}.")

# --- Export des données ---
st.sidebar.header("📥 Export")
if st.sidebar.button("Télécharger les données filtrées"):
    csv = df_filtered.to_csv(index=False, sep=';').encode('utf-8')
    st.sidebar.download_button(
        label="Télécharger le CSV",
        data=csv,
        file_name=f"matchs_france_{decade[0]}-{decade[1]}.csv",
        mime='text/csv'
    )

