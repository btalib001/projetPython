import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Statistiques Générales",page_icon="🇫🇷",layout="wide")
url_logo = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/image/Logo_F%C3%A9d%C3%A9ration_Fran%C3%A7aise_Football_2022.svg"
st.logo(url_logo, size="large", link="https://www.fff.fr/selection/2-equipe-de-france/index.html")

url = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/df_matches.csv"

df_matchs = pd.read_csv(url)

#remplace les NaN par 0
df_matchs.fillna(0, inplace=True)

#renommage des colonnes
df_matchs.rename(columns={'X4':'Match',"X5":"Score","X6":"Compétition","outcome":"Résultat","year":"Année","adversaire":"Adversaire","score_france":"Score France","score_adversaire":"Score adversaire","penalty_france":"Penalty France","penalty_adversaire":"Penalty adversaire"}, inplace=True)

#suppression des colonnes non pertinentes
df_matchs.drop(columns=['X2','no'], inplace=True)

#remplacement de draw par nul, win par victoire, loss par défaite
df_matchs.replace({"Résultat":{"draw":"nul","win":"victoire","loss":"défaite"}}, inplace=True)

# Barre latérale pour la décennie
with st.sidebar:
    st.header("🎛️ Filtres")
    decade = st.slider(
        "Décennie",
        min_value=1900,
        max_value=2020,
        value=(1950, 2020),
        step=10
    )

# Filtrer les données par décennie
df_filtered = df_matchs[(df_matchs['Année'] >= decade[0]) & (df_matchs['Année'] <= decade[1])]



# Section 1 : Tableau de bord général 
st.header("📊 Tableau de bord")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Matchs joués", len(df_filtered))
col2.metric("Victoires", (df_filtered['Résultat'] == 'victoire').sum())
col3.metric("Défaites", (df_filtered['Résultat'] == 'défaite').sum())
col4.metric("Nuls", (df_filtered['Résultat'] == 'nul').sum())

# Graphique : Évolution des buts par décennie
df_filtered['Décennie'] = (df_filtered['Année'] // 10) * 10
buts_par_décennie = df_filtered.groupby('Décennie').agg({'Score France': 'mean','Score adversaire': 'mean'}).reset_index()

fig_buts = px.line(
    buts_par_décennie,
    x='Décennie',
    y=['Score France', 'Score adversaire'],
    title=f"Moyenne de buts marqués/concédés par décennie ({decade[0]}-{decade[1]})",
    labels={'value': 'Nombre de buts', 'variable': ''},
    color_discrete_sequence=['#0055A4', '#EF4135']  # Couleurs de l'équipe de France
)
st.plotly_chart(fig_buts, use_container_width=True)

# Camembert : Répartition des résultats
fig_pie = px.pie(
    df_filtered,
    names='Résultat',
    title=f"Répartition des résultats ({decade[0]}-{decade[1]})",
    color='Résultat',
    color_discrete_map={"victoire":"#0055A4","défaite":"#EF4135","nul":"#e2e2da"},
    hole=0.3
)
st.plotly_chart(fig_pie, use_container_width=True)

# Section 2 : Résultats selon adversaire
st.header("Choisir un adversaire")

# Liste des adversaires disponibles (filtrés par décennie)
adversaires = df_filtered['Adversaire'].unique()
if len(adversaires) == 0:
    st.error(f"Aucun adversaire trouvé entre {decade[0]} et {decade[1]}. Elargis la période.")
    st.stop()

adversaire = st.selectbox("",adversaires)

# Filtrer les matchs contre cet adversaire (avec la décennie appliquée)
matches_adversaire = df_filtered[df_filtered['Adversaire'] == adversaire]

st.subheader(f"📊 Bilan contre {adversaire} ({decade[0]}-{decade[1]})")
col1, col2, col3 = st.columns(3)
col1.metric("Victoires", (matches_adversaire['Résultat'] == 'victoire').sum())
col2.metric("Défaites", (matches_adversaire['Résultat'] == 'défaite').sum())
col3.metric("Nuls", (matches_adversaire['Résultat'] == 'nul').sum())



# Derniers matchs
st.subheader(f"📜 Derniers matchs contre {adversaire} ({decade[0]}-{decade[1]})")
if len(matches_adversaire) > 0:
    st.dataframe(
        matches_adversaire.sort_values('Année', ascending=False)[['date', 'Score France', 'Score adversaire', 'Résultat']].head(5),
        hide_index=True,
        use_container_width=True
    )
else:
    st.info(f"Aucun match historique disponible contre {adversaire} entre {decade[0]} et {decade[1]}.")

# Export des données
st.sidebar.header("📥 Export")
if st.sidebar.button("Télécharger les données filtrées"):
    csv = df_filtered.to_csv(index=False, sep=';').encode('utf-8')
    st.sidebar.download_button(
        label="Télécharger le CSV",
        data=csv,
        file_name=f"matchs_france_{decade[0]}-{decade[1]}.csv",
        mime='text/csv'
    )



