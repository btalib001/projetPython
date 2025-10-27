import pandas as pd
import streamlit as st
import plotly.express as px
#import streamlit.components.v1 as components
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,)
import numpy as np
from urllib.parse import quote  # For URL-encoding Wikipedia page titles

url = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/df_matches.csv"

df = pd.read_csv(url)

#remplace les NaN par 0
df.fillna(0, inplace=True)

#renommage des colonnes
df.rename(columns={'X4':'Match',"X5":"Score","X6":"Compétition","outcome":"Résultat","year":"Année"}, inplace=True)

#suppression des colonnes non pertinentes
df.drop(columns=['X2','date','no'], inplace=True)

#remplacement de URSS-France dans la colonne adversaire par URSS
df.replace({"adversaire":{"URSS- France":"URSS"}}, inplace=True)

st.title("Historique des matches de l'équipe de France de football")
st.write("du 1er mai 1904 au 26 juin 2018")

##affichage du dataframe avec menu de filtres

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
        Adds a UI on top of a dataframe to let viewers filter columns

        Args:
            df (pd.DataFrame): Original dataframe

        Returns:
            pd.DataFrame: Filtered dataframe
        """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if isinstance(df[column],pd.CategoricalDtype) or df[column].nunique() < 1000:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=1.0,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

st.dataframe(filter_dataframe(df),hide_index=True)

# pie chart avec le résultat des matchs

win_count = df[df["Résultat"] == "win"].count()["Résultat"]
loss_count = df[df["Résultat"] == "loss"].count()["Résultat"]
draw_count = df[df["Résultat"] == "draw"].count()["Résultat"]


PieChartOutcome = {"names":["matchs nuls","victoires","défaites"], "counts" :[draw_count,win_count,loss_count]}

dataframe = pd.DataFrame(PieChartOutcome)
data_figure = px.pie(dataframe, values="counts", names="names", title="Résultat des matchs")
#data_figure = px.pie(dataframe, values="counts", names="names", color="names", title="Résultat des matchs", color_discrete_map={"victoires":"green","défaites":"red","matchs nuls":"grey"})

st.plotly_chart(data_figure)

#evolution buts marqués, buts encaissés, pénaltys marqués, pénaltys encaissés
x = np.arange(1,836)
buts_inscrits = np.cumsum(df["score_france"])
buts_encaisses = np.cumsum(df["score_adversaire"])

butsData = {"x":x,"buts inscrits":buts_inscrits,"buts encaissés":buts_encaisses}
df_butsData = pd.DataFrame(butsData)
fig1 = px.line(df_butsData, x="x", y=["buts inscrits","buts encaissés"], labels={"x":"Nombre de matchs joués", "value":"Nombre de buts"})

penaltys_inscrits = np.cumsum(df["penalty_france"])
penaltys_encaisses = np.cumsum(df["penalty_adversaire"])

penaltyData = {"x":x,"penaltys inscrits":penaltys_inscrits,"penaltys encaissés":penaltys_encaisses}
df_penaltyData = pd.DataFrame(penaltyData)
fig2 = px.line(df_penaltyData, x="x", y=["penaltys inscrits","penaltys encaissés"], labels={"x":"Nombre de matchs joués", "value":"Nombre de penaltys"})


tab1, tab2 = st.tabs(["évolution du nombre de buts marqués et encaissés","évolution du nombre de penaltys marqués et encaissés"])

with tab1:
    st.plotly_chart(fig1)

with tab2:
    st.plotly_chart(fig2)

#pie chart des adversaires de la france

adversaires = df['adversaire']
teams = []
counts = []
for index, value in adversaires.value_counts().items():
    teams.append(index)
    counts.append(value)

PieChartAdversaires = {"teams":teams, "counts":counts}
df_adversaires = pd.DataFrame(PieChartAdversaires)

fig_adversaires = px.pie(df_adversaires, names="teams", values="counts", title="Adversaires rencontrés")
st.plotly_chart(fig_adversaires)

#match avec 0,1 entre 2 et 4 buts marqués, +5 buts marqués
#match avec 0,1, entre 2 et 4 buts encaissés, +5 buts encaissés

inscrit_0 = df[df["score_france"]==0].count()["score_france"]
inscrit_1 = df[df["score_france"]==1].count()["score_france"]
inscrit_24 = df[(df["score_france"]>=2) & (df["score_france"]<=4)].count()["score_france"]
inscrit_5 = df[df["score_france"]>=5].count()["score_france"]

noms_inscrits = ["0 but","1 but","entre 2 et 4 buts","plus de 5 buts"]
buts_inscrits = [inscrit_0, inscrit_1, inscrit_24, inscrit_5]

PieInscrits = {"names":noms_inscrits, "nombre de buts":buts_inscrits}
frameInscrit = pd.DataFrame(PieInscrits)

figInscrits = px.pie(frameInscrit, names="names", values="nombre de buts")

encaisses_0 = df[df["score_adversaire"]==0].count()["score_adversaire"]
encaisses_1 = df[df["score_adversaire"]==1].count()["score_adversaire"]
encaisses_24 = df[(df["score_adversaire"]>=2) & (df["score_adversaire"]<=4)].count()["score_adversaire"]
encaisses_5 = df[df["score_adversaire"]>=5].count()["score_adversaire"]

noms_encaisses = ["0 but","1 but","entre 2 et 4 buts","plus de 5 buts"]
buts_encaisses = [encaisses_0, encaisses_1, encaisses_24, encaisses_5]

PieEncaisses = {"noms":noms_encaisses, "nombre de buts":buts_encaisses}
frameEncaisses = pd.DataFrame(PieEncaisses)

figEncaisses = px.pie(frameEncaisses, names="noms",values="nombre de buts")

tab1, tab2 = st.tabs(["Statistiques des matchs selon le nombre de buts inscrits par la France","Statistiques des matchs selon le nombre de buts encaissés par la France"])
with tab1:
    st.plotly_chart(figInscrits)

with tab2:
    st.plotly_chart(figEncaisses)



#meilleurs buteurs, passeurs sur une nouvelle page intitulée Statistiques Individuelles

# Create a Pandas DataFrame
url1 = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/buteurs.csv"
df1 = pd.read_csv(url1,sep=";")

# Function to create a Wikipedia link (French Wikipedia)
def make_wiki_link(name):
    encoded_name = quote(name.replace(' ', '_'))  # URL-encode for Wikipedia URL
    return f'<a href="https://fr.wikipedia.org/wiki/{encoded_name}" target="_blank">{name}</a>'

# Apply the link transformation to the 'Joueur' column
df1['Joueur'] = df1['Joueur'].apply(make_wiki_link)

# Streamlit app
st.title("Meilleurs Buteurs de l'Équipe de France")
st.write("Cliquez sur le nom d'un joueur pour visiter sa page Wikipedia (en français).")

# Display the DataFrame with HTML rendering enabled for links
st.write(df1.to_html(escape=False, index=False), unsafe_allow_html=True)



# Create a Pandas DataFrame
url2 = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/passeurs.csv"
df2 = pd.read_csv(url2,sep=";")

# Apply the link transformation to the 'Joueur' column
df2['Joueur'] = df2['Joueur'].apply(make_wiki_link)

# Streamlit app
st.title("Meilleurs Passeurs de l'Équipe de France")
st.write("Cliquez sur le nom d'un joueur pour visiter sa page Wikipedia (en français).")

# Display the DataFrame with HTML rendering enabled for links
st.write(df2.to_html(escape=False, index=False), unsafe_allow_html=True)
