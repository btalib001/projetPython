import streamlit as st
import pandas as pd
from urllib.parse import quote  # pour l' URL-encoding du titre des pages Wikipedia

st.set_page_config(page_title="Statistiques Individuelles", page_icon=":trophy:",layout="centered",)
st.title("🏆 Statistiques Individuelles")

url_logo = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/image/Logo_F%C3%A9d%C3%A9ration_Fran%C3%A7aise_Football_2022.svg"
st.logo(url_logo, size="large", link="https://www.fff.fr/selection/2-equipe-de-france/index.html")

# Fonction qui créé un lien Wikipedia (Wikipedia fr)
def make_wiki_link(name):
    #gestion des noms spéciaux (qui ne renvoient pas directement sur leur page wikipédia)
    special_names = ["Henri Michel","Henri Guérin","Jean Nicolas"]
    if name in special_names:
        encoded_name = quote(name.replace(" ","_"))+"_(football)"
    else:
        encoded_name = quote(name.replace(' ', '_'))  # encodage URL pour Wikipedia
    return f'<a href="https://fr.wikipedia.org/wiki/{encoded_name}" target="_blank">{name}</a>'



# Creation d'un dataframe Pandas pour chaque tableau
url1 = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/buteurs.csv"
df1 = pd.read_csv(url1,sep=";")

url2 = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/passeurs.csv"
df2 = pd.read_csv(url2,sep=";")

url3 = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/NbSelections.csv"
df3 = pd.read_csv(url3)

url4 = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/Selectionneurs.csv"
df4 = pd.read_csv(url4)


# Application de la fonction make_wiki_link
df1['Joueur'] = df1['Joueur'].apply(make_wiki_link)
df2['Joueur'] = df2['Joueur'].apply(make_wiki_link)
df3['Joueur'] = df3['Joueur'].apply(make_wiki_link)
df4['Sélectionneur'] = df4['Sélectionneur'].apply(make_wiki_link)



tab1,tab2,tab3,tab4 = st.tabs(["Les plus sélectionnés","Les meilleurs buteurs","Les meilleurs passeurs","Les sélectionneurs"])


with tab1:
    st.write("*Cliquez sur le nom d'un joueur pour visiter sa page Wikipedia.*")
    col1,col2,col3 = st.columns([0.25,3.5,0.25])
    col2.subheader('Joueurs les plus sélectionnés')
    col2.write(df3.to_html(escape=False, index=False), unsafe_allow_html=True)

with tab2:
    st.write("*Cliquez sur le nom d'un joueur pour visiter sa page Wikipedia.*")
    col1,col2,col3 = st.columns([0.25,3.5,0.25])
    col2.subheader("Meilleurs Buteurs de l'Équipe de France")
    col2.write(df1.to_html(escape=False, index=False), unsafe_allow_html=True)

with tab3:
    st.write("*Cliquez sur le nom d'un joueur pour visiter sa page Wikipedia.*")
    col1,col2,col3 = st.columns([0.25,3.5,0.25])
    col2.subheader("Meilleurs Passeurs de l'Équipe de France")
    col2.write(df2.to_html(escape=False, index=False), unsafe_allow_html=True)

with tab4:
    st.write("*Cliquez sur le nom d'un sélectionneur pour visiter sa page Wikipedia.*")
    col1,col2,col3 = st.columns([0.25,3.5,0.25])
    col2.subheader("Les Sélectionneurs de l'équipe de France de football")
    col2.write(df4.to_html(escape=False, index=False), unsafe_allow_html=True)