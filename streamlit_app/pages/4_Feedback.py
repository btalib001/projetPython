import streamlit as st
from supabase import create_client, Client
import datetime
import pandas as pd

#Configuration de la page
st.set_page_config(page_title="Feedback App", page_icon="💬", layout="centered")
st.title("💬 Partagez votre avis !")


url_logo = "https://raw.githubusercontent.com/btalib001/projetPython/refs/heads/main/image/Logo_F%C3%A9d%C3%A9ration_Fran%C3%A7aise_Football_2022.svg"
st.logo(url_logo, size="large", link="https://www.fff.fr/selection/2-equipe-de-france/index.html")

#Configuration Supabase

# Récupération des secrets, c'est la marche à suivre. Toujours garder les clés supabase dans les secret streamlit dans un fichier ".streamlit/secrets.toml"
#si on voulait déployer l'app sur le cloud, on peut déclarer facilement les clés secrets dans les paramètres 
#url = st.secrets["SUPABASE_URL"]
#key = st.secrets["SUPABASE_ANON_KEY"]


SUPABASE_URL = "https://rtbgmosauydbvtgpghzh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ0Ymdtb3NhdXlkYnZ0Z3BnaHpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE3NTY0NDIsImV4cCI6MjA3NzMzMjQ0Mn0.Uzox6OBxihh4h7q8dIk23D2gOpnVANlIU1sPIZfLbP0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

#Formulaire de feedback
with st.form("feedback_form"):
    nom = st.text_input("Votre nom (optionnel)")
    email = st.text_input("Votre e-mail (optionnel)")
    satisfaction = st.slider("Votre satisfaction", 0, 10, 5)
    commentaire = st.text_area("Votre commentaire")

    soumettre = st.form_submit_button("📨 Envoyer")

if soumettre:
    if commentaire.strip() == "":
        st.warning("Merci d'ajouter un commentaire.")
    else:
        data = {
            "nom": nom,
            "email": email,
            "satisfaction": satisfaction,
            "commentaire": commentaire,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        supabase.table("feedback_app").insert(data).execute()
        st.success("✅ Merci pour votre feedback !")
        st.balloons()

# Affichage des feedbacks
if st.checkbox("📊 Voir les feedbacks"):
    result = supabase.table("feedback_app").select("*").order("date", desc=True).execute()
    df = pd.DataFrame(result.data)
    if not df.empty:
        st.dataframe(df,hide_index=True)
    else:

        st.info("Aucun feedback enregistré pour l’instant 😇")

