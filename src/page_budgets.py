import os
import streamlit as st
import requests

from jours_utils import jour_cible


INGESTION_SERVICE_URL = os.environ["INGESTION_SERVICE_URL"]

categories = [
    {"id": -1, "nom": "Toutes"},
    {"id": 1, "nom": "Indéterminée"},
    {"id": 2, "nom": "Fruits & légumes"},
    {"id": 3, "nom": "Viandes & poissons"},
    {"id": 4, "nom": "Produits laitiers"},
    {"id": 5, "nom": "Épicerie salée"},
    {"id": 6, "nom": "Épicerie sucrée"},
    {"id": 7, "nom": "Surgelés"},
    {"id": 8, "nom": "Frais"},
    {"id": 9, "nom": "Eaux"},
    {"id": 10, "nom": "Boissons alcoolisées"},
    {"id": 11, "nom": "Boissons non alcoolisées (hors eaux)"},
]

debut_periode_client = {1: 5, 2: 30, 3: 2}


def nom_categorie(categorie_id: int) -> str:
    return next((c["nom"] for c in categories if c["id"] == categorie_id), None)


def page_budgets():
    client_id = st.session_state.get("username", None)
    st.header("Budgets")

    # Création d'une liste de noms pour le selectbox
    categorie_noms = [cat["nom"] for cat in categories]

    # Sélecteur de catégorie
    selected_nom = st.selectbox("Choisissez une catégorie :", categorie_noms)

    # Récupération de l'id correspondant
    selected_cat = next((cat for cat in categories if cat["nom"] == selected_nom), None)
    categorie_id = selected_cat["id"] if selected_cat else None

    if categorie_id is not None:
        url = f"{INGESTION_SERVICE_URL}/clients/{client_id}/depenses"
        if categorie_id != -1:
            url = f"{INGESTION_SERVICE_URL}/clients/{client_id}/depenses?categorie_id={categorie_id}"
        else:
            url = f"{INGESTION_SERVICE_URL}/clients/{client_id}/depenses"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            montant_formate = f"{data:,.2f}".replace(",", " ").replace(".", ",")
            st.markdown(
                f"""
                <div style='font-size: 2.5em; font-weight: bold; color: #2E86C1;'>
            url = f"{INGESTION_SERVICE_URL}/clients/{client_id}/depenses?categorie_id={categorie_id}"
                    Dépenses depuis {jour_cible(debut_periode_client.get(client_id, 1))} {nom_categorie(categorie_id)} {montant_formate} €
                </div>
                """,
                unsafe_allow_html=True,
            )

        except requests.RequestException as e:
            st.error(f"Erreur lors de la récupération des données : {e}")
