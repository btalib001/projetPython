import pandas as pd
import streamlit as st

#meilleurs buteurs, passeurs sur une nouvelle page intitulée Statistiques Individuelles

url1 = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/buteurs.csv"
df = pd.read_csv(url1,sep=";")

st.title("Statistiques individuelles")

st.write("Classement des 20 meilleurs buteurs de l'équipe de France de football")
st.dataframe(df,hide_index=True)

url2 = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/passeurs.csv"
df2 = pd.read_csv(url2,sep=";")
st.write("Classement des 10 meilleurs passeurs de l'équipe de France de football")
st.dataframe(df2,hide_index=True)