import streamlit as st
from supabase import create_client, Client
import datetime
import pandas as pd

# --- Configuration de la page ---
st.set_page_config(page_title="Feedback App", page_icon="💬", layout="centered")
st.title("💬 Partagez votre avis !")

# --- Configuration Supabase ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Formulaire de feedback ---
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

# --- Affichage feedbacks ---
if st.checkbox("📊 Voir les feedbacks"):
    result = supabase.table("feedback_app").select("*").order("date", desc=True).execute()
    df = pd.DataFrame(result.data)
    if not df.empty:
        st.dataframe(df,hide_index=True)
    else:
        st.info("Aucun feedback enregistré pour l’instant 😇")
