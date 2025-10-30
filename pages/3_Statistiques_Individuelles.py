import streamlit as st
import pandas as pd
from urllib.parse import quote  # For URL-encoding Wikipedia page titles

st.set_page_config(page_title="Statistiques Individuelles", page_icon=":trophy:",layout="wide")
st.title("🏆 Statistiques Individuelles")
st.write("*Cliquez sur le nom pour visiter sa page Wikipedia.*")

url_logo = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/image/Logo_F%C3%A9d%C3%A9ration_Fran%C3%A7aise_Football_2022.svg"
st.logo(url_logo, size="large", link="https://www.fff.fr/selection/2-equipe-de-france/index.html")

# Function to create a Wikipedia link (French Wikipedia)
def make_wiki_link(name):
    encoded_name = quote(name.replace(' ', '_'))  # URL-encode for Wikipedia URL
    return f'<a href="https://fr.wikipedia.org/wiki/{encoded_name}" target="_blank">{name}</a>'

url3 = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/NbSelections.csv"
df3 = pd.read_csv(url3)
df3['Joueur'] = df3['Joueur'].apply(make_wiki_link)

url4 = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/Selectionneurs.csv"
df4 = pd.read_csv(url4)
df4['Sélectionneur'] = df4['Sélectionneur'].apply(make_wiki_link)


col1,col2 = st.columns(2)
with col1:
    st.subheader('Joueurs les plus sélectionnés')
    st.write(df3.to_html(escape=False, index=False), unsafe_allow_html=True)

with col2:
    st.subheader("Les 10 derniers sélectionneurs de l'équipe de France de football")
    st.write(df4.to_html(escape=False, index=False), unsafe_allow_html=True)


# Create a Pandas DataFrame
url1 = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/buteurs.csv"
df1 = pd.read_csv(url1,sep=";")

# Apply the link transformation to the 'Joueur' column
df1['Joueur'] = df1['Joueur'].apply(make_wiki_link)




# Create a Pandas DataFrame
url2 = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/passeurs.csv"
df2 = pd.read_csv(url2,sep=";")

# Apply the link transformation to the 'Joueur' column
df2['Joueur'] = df2['Joueur'].apply(make_wiki_link)



col1, col2 = st.columns(2)
with col1:
    st.subheader("Meilleurs Buteurs de l'Équipe de France")
    st.write(df1.to_html(escape=False, index=False), unsafe_allow_html=True)

with col2:
    st.subheader("Meilleurs Passeurs de l'Équipe de France")
    st.write(df2.to_html(escape=False, index=False), unsafe_allow_html=True)