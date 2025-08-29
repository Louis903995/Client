from dotenv import load_dotenv
import streamlit as st
from page_budgets import page_budgets
from page_tickets import page_tickets
from upload_page import page_upload
from courbe_page import page_courbe
import os 
import requests


load_dotenv(dotenv_path=".env", override=False) 

INGESTION_SERVICE_URL = os.environ["INGESTION_SERVICE_URL"]




# def api_authenticate(email: str):
#     """Récupère un client par email """
#     response = requests.get(f"{INGESTION_SERVICE_URL}/clients")  
#     if response.status_code == 200:
#         clients = response.json()
#         for client in clients:
#             if client["email_client"] == email:
#                 return client
#     return None


def fake_azure_auth():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if not st.session_state["authenticated"]:
        st.title("Authentification requise")
        with st.form("auth_form"):
            username = st.text_input("Nom d'utilisateur Azure")
            password = st.text_input("Mot de passe", type="password")
            submit = st.form_submit_button("Se connecter")
            if submit:
                if username and password:
                    response = requests.get(f"{INGESTION_SERVICE_URL}/clients/{username}")  
                    if response.status_code == 200:
                        st.session_state["client"] = response.json()
                        st.session_state["authenticated"] = True
                        st.session_state["username"] = username
                        st.success("Authentifié !")
                        st.rerun()
                else:
                    st.error("Identifiants invalides.")
        st.stop()

def page_logout():
    st.header("Déconnexion")
    if st.button("Se déconnecter"):
        st.session_state["authenticated"] = False
        st.success("Déconnecté !")
        st.rerun()


def main():
    fake_azure_auth()

    menu_items = {
        "Accueil": "home",
        "Ajouter un ticket": "upload",
        "Tickets": "tickets",
        "Budgets": "budgets",
        "Dépenses et prévisions": "courbe",
        "Déconnexion": "logout",
    }
    st.sidebar.title("Menu")
    choix = st.sidebar.radio("Navigation", list(menu_items.keys()))

    if menu_items[choix] == "home":
        client = st.session_state["client"]
        st.title(f"Bonjour {client['prenom_client']} {client['nom_client']}")
        st.write("Utilisez le menu à gauche pour naviguer.")
    elif menu_items[choix] == "upload":
        page_upload()
    elif menu_items[choix] == "tickets":
        page_tickets()
    elif menu_items[choix] == "courbe":
        page_courbe()
    elif menu_items[choix] == "budgets":
        page_budgets()
    elif menu_items[choix] == "logout":
        page_logout()



if __name__ == "__main__":
    main()
