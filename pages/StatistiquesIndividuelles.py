import streamlit as st
import pandas as pd
from urllib.parse import quote  # For URL-encoding Wikipedia page titles




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