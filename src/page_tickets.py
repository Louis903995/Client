import os
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

INGESTION_SERVICE_URL = os.environ["INGESTION_SERVICE_URL"]


def page_tickets():
    client_id = st.session_state.get("username", None)
    st.title("Vos tickets")

    # Champs calendrier
    col1, col2 = st.columns(2)
    with col1:
        date_from = st.date_input("À partir de", value=None, key="date_from")
    with col2:
        date_to = st.date_input("Jusqu'à", value=None, key="date_to")

    # Construction de la query string
    params = {}
    qs_display = []
    if date_from:
        params["from"] = date_from.strftime("%Y-%m-%d")
        qs_display.append(f"from={date_from.strftime('%d/%m/%Y')}")
    if date_to:
        params["to"] = date_to.strftime("%Y-%m-%d")
        qs_display.append(f"to={date_to.strftime('%d/%m/%Y')}")



    # Appel de l'API
    url = f"{INGESTION_SERVICE_URL}/clients/{client_id}/tickets"
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            st.write(f"Nombre de tickets récupérés : {len(data)}")

            tickets = []
            ticket_lines = {}
            for ticket in data:
                date_ticket = datetime.strptime(
                    ticket["date_heure_ticket"], "%Y-%m-%dT%H:%M:%S"
                )
                date_formatted = date_ticket.strftime("%d/%m/%Y %H:%M")
                label = f"Ticket du {date_formatted} - {ticket['enseigne_nom']}"
                tickets.append({"label": label, "id": ticket["ticket_id"]})
                lines = []
                for ligne in ticket.get("lignes", []):
                    lines.append(
                        {
                            "Produit": ligne["libelle_produit"],
                            "Catégorie": ligne["nom_categorie_produit"],
                            "Quantité": ligne["quantite"],
                            "Prix unitaire": f"{ligne['montant_total_ligne']:,.2f}".replace(
                                ",", "X"
                            )
                            .replace(".", ",")
                            .replace("X", ".")
                            if ligne["montant_total_ligne"] is not None
                            else "",
                            "Montant TTC": f"{ligne['montant_total_ligne']:,.2f}".replace(
                                ",", "X"
                            )
                            .replace(".", ",")
                            .replace("X", "."),
                        }
                    )
                ticket_lines[ticket["ticket_id"]] = lines

            if tickets:
                choice = st.selectbox(
                    "Sélectionnez un ticket pour voir le détail",
                    tickets,
                    format_func=lambda t: t["label"],
                )
                selected_ticket_id = choice["id"]
                lines = ticket_lines[selected_ticket_id]
                if lines:
                    df = pd.DataFrame(lines)
                    st.dataframe(df)
                else:
                    st.info("Aucune ligne pour ce ticket.")
            else:
                st.info("Aucun ticket à afficher.")
        else:
            st.error(
                f"Erreur lors de la récupération de la table : {response.status_code}"
            )
    except Exception as e:
        st.error(f"Erreur d'appel API: {e}")
