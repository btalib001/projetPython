import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,)

st.set_page_config(
    page_title="Bienvenue dans le monde de l'équipe de France de football",
    page_icon=":soccer:",
    layout="wide",
)

#affichage d'un logo
url_logo = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/image/Logo_F%C3%A9d%C3%A9ration_Fran%C3%A7aise_Football_2022.svg"
st.logo(url_logo, size="large", link="https://www.fff.fr/selection/2-equipe-de-france/index.html")
#link permet de renvoyer l'utilisateur vers une page lorsqu'il clique sur le logo
#ici, le site de l'équipe de France A
#pour avoir les dernières actualités notamment


st.title("Historique des matchs de l'équipe de France de football")
st.write("du 1er mai 1904 au 26 juin 2018")


url = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/df_matches.csv"

df_matchs = pd.read_csv(url)

#remplace les NaN par 0
df_matchs.fillna(0, inplace=True)

#renommage des colonnes
df_matchs.rename(columns={'X4':'Match',"X5":"Score","X6":"Compétition","outcome":"Résultat","year":"Année","adversaire":"Adversaire","score_france":"Score France","score_adversaire":"Score adversaire","penalty_france":"Penalty France","penalty_adversaire":"Penalty adversaire"}, inplace=True)

#suppression des colonnes non pertinentes
df_matchs.drop(columns=['X2','date','no'], inplace=True)

#remplacement de draw par nul, win par victoire, loss par défaite
df_matchs.replace({"Résultat":{"draw":"nul","win":"victoire","loss":"défaite"}}, inplace=True)


##affichage du dataframe avec menu de filtres

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
        Ajoute une interface utilisateur au-dessus d’un dataframe
        afin de permettre aux utilisateurs de filtrer les colonnes

        Arguments:
            df (pd.DataFrame) : le dataframe original

        Returns:
            pd.DataFrame: le dataframe filtré
        """
    modify = st.checkbox("Filtres")

    if not modify:
        return df

    df = df.copy()

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filtrer le datafram selon", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            
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

st.dataframe(filter_dataframe(df_matchs),hide_index=True)

st.write("Dans cette application, vous pourrez accéder à de nombreuses statistiques concernant l'équipe de France de football :fr: :soccer:")
st.write("*Les données traitées proviennent du site data.gouv et ne concernent que la période entre 1er mai 1904 et le 26 juin 2018.*")



