from dotenv import load_dotenv
import streamlit as st
from page_budgets import page_budgets
from page_tickets import page_tickets
from upload_page import page_upload
from courbe_page import page_courbe

load_dotenv(dotenv_path=".env", override=False)


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
        "Nouvelle étiquette": "upload",
        "Tickets": "tickets",
        "Budgets": "budgets",
        "Afficher la courbe": "courbe",
        "Déconnexion": "logout",
    }
    st.sidebar.title("Menu")
    choix = st.sidebar.radio("Navigation", list(menu_items.keys()))

    if menu_items[choix] == "home":
        st.title("Contre la vie chère.")
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
