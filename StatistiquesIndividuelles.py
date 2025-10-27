import streamlit as st
import pandas as pd
from urllib.parse import quote  # For URL-encoding Wikipedia page titles


# Hardcoded data from the first CSV (goalscorers ranking)
data = {
    'Rang': [1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 11, 12, 13, 14, 15, 15, 17, 18, 18, 20, 20],
    'Joueur': [
        'Olivier Giroud', 'Kylian Mbappé', 'Thierry Henry', 'Antoine Griezmann',
        'Michel Platini', 'Karim Benzema', 'David Trezeguet', 'Zinédine Zidane',
        'Just Fontaine', 'Jean-Pierre Papin', 'Youri Djorkaeff', 'Sylvain Wiltord',
        'Jean Vincent', 'Jean Nicolas', 'Paul Nicolas', 'Éric Cantona',
        'Jean Baratte', 'Roger Piantoni', 'Raymond Kopa', 'Franck Ribéry',
        'Laurent Blanc'
    ],
    'Poste': [
        'Attaquant', 'Attaquant', 'Attaquant', 'Attaquant', 'Milieu', 'Attaquant',
        'Attaquant', 'Milieu', 'Attaquant', 'Attaquant', 'Milieu', 'Attaquant',
        'Attaquant', 'Attaquant', 'Attaquant', 'Attaquant', 'Attaquant', 'Attaquant',
        'Milieu', 'Milieu', 'Défenseur'
    ],
    'Période': [
        '2011-2024', 'Depuis 2017', '1997-2010', '2014-2024', '1976-1987', '2007-2022',
        '1998-2008', '1994-2006', '1953-1960', '1986-1995', '1993-2002', '1999-2006',
        '1953-1961', '1933-1938', '1920-1931', '1987-1995', '1944-1952', '1952-1961',
        '1952-1962', '2006-2014', '1989-2000'
    ],
    'Durée': [
        '12 ans, 241 jours', '8 ans, 166 jours', '12 ans, 254 jours', '10 ans, 188 jours',
        '11 ans, 33 jours', '15 ans, 77 jours', '10 ans, 58 jours', '11 ans, 326 jours',
        '6 ans, 360 jours', '8 ans, 326 jours', '8 ans, 241 jours', '7 ans, 278 jours',
        '7 ans, 305 jours', '5 ans, 295 jours', '11 ans, 28 jours', '7 ans, 159 jours',
        '7 ans, 323 jours', '8 ans, 316 jours', '10 ans, 37 jours', '7 ans, 282 jours',
        '11 ans, 208 jours'
    ],
    'Sélections': [137, 93, 123, 137, 72, 97, 71, 108, 21, 54, 82, 92, 46, 25, 35, 45, 32, 37, 45, 81, 97],
    'Ratio': [0.42, 0.57, 0.41, 0.32, 0.57, 0.38, 0.48, 0.29, 1.43, 0.56, 0.34, 0.28, 0.48, 0.84, 0.57, 0.44, 0.59, 0.49, 0.4, 0.2, 0.16],
    'Buts': [57, 53, 51, 44, 41, 37, 34, 31, 30, 30, 28, 26, 22, 21, 20, 20, 19, 18, 18, 16, 16]
}

# Create a Pandas DataFrame
df = pd.DataFrame(data)

# Function to create a Wikipedia link (French Wikipedia)
def make_wiki_link(name):
    encoded_name = quote(name.replace(' ', '_'))  # URL-encode for Wikipedia URL
    return f'<a href="https://fr.wikipedia.org/wiki/{encoded_name}" target="_blank">{name}</a>'

# Apply the link transformation to the 'Joueur' column
df['Joueur'] = df['Joueur'].apply(make_wiki_link)

# Streamlit app
st.title("Meilleurs Buteurs de l'Équipe de France")
st.write("Cliquez sur le nom d'un joueur pour visiter sa page Wikipedia (en français).")

# Display the DataFrame with HTML rendering enabled for links
st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)



# Hardcoded data from the image (semicolon-separated CSV equivalent)
data = {
    'Rang': [1, 2, 3, 4, 5, 5, 5, 8, 9, 9],
    'Nom': [
        'Kylian Mbappé', 'Antoine Griezmann', 'Thierry Henry', 'Zinédine Zidane',
        'Raymond Kopa', 'Michel Platini', 'Youri Djorkaeff', 'Sylvain Wiltord',
        'Franck Ribéry', 'Karim Benzema'
    ],
    'Période': [
        '2017-', '2014-2024', '1997-2010', '1994-2006', '1952-1962',
        '1976-1987', '1993-2002', '1999-2006', '2006-2014', '2007-2022'
    ],
    'Passes décisives': [33, 30, 27, 25, 20, 20, 20, 18, 17, 17],
    'Sélections': [93, 137, 123, 108, 45, 72, 82, 92, 81, 97]
}

# Create a Pandas DataFrame
df = pd.DataFrame(data)

# Apply the link transformation to the 'Nom' column
df['Nom'] = df['Nom'].apply(make_wiki_link)

# Streamlit app
st.title("Meilleurs Passeurs de l'Équipe de France")
st.write("Cliquez sur le nom d'un joueur pour visiter sa page Wikipedia (en français).")

# Display the DataFrame with HTML rendering enabled for links
st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)