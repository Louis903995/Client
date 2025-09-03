import requests
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime, timedelta
import numpy as np

INGESTION_SERVICE_URL = os.environ["INGESTION_SERVICE_URL"]

def page_courbe():
    st.title("Dépenses et prévisions - Août 2025")

    # ID client
    client_id = 1
    url = f"{INGESTION_SERVICE_URL}/clients/{client_id}/allures"

    # Récupération des données via l'API
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # Extraire les dates et valeurs
        depenses_constatees = [item["v"] for item in data.get("depense_constate", [])]
        depenses_constatees_dates = [datetime.fromisoformat(item["d"]) for item in data.get("depense_constate", [])]
        depenses_predites = [item["v"] for item in data.get("depense_predite", [])]
        depenses_predites_dates = [datetime.fromisoformat(item["d"]) for item in data.get("depense_predite", [])]
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données API : {e}")
        depenses_constatees = []
        depenses_constatees_dates = []
        depenses_predites = []
        depenses_predites_dates = []

    # Créer la liste complète des semaines en combinant les dates constatées et prédites
    semaines = sorted(list(set(depenses_constatees_dates + depenses_predites_dates)))

    # Compléter les listes pour correspondre aux semaines
    depenses_constatees_dict = dict(zip(depenses_constatees_dates, depenses_constatees))
    depenses_predites_dict = dict(zip(depenses_predites_dates, depenses_predites))

    depenses_constatees_aligned = [depenses_constatees_dict.get(d, np.nan) for d in semaines]
    depenses_predites_aligned = [depenses_predites_dict.get(d, np.nan) for d in semaines]

    # Dépenses combinées (priorité constatée, sinon prédite)
    depenses = [c if not np.isnan(c) else p for c, p in zip(depenses_constatees_aligned, depenses_predites_aligned)]

    # Budget du client 
    budget = st.session_state["client"]["budget_client"]    
    
    # Calcul du point de dépassement
    depassement_x = None
    depassement_label = None
    for i in range(len(depenses)-1):
        y1, y2 = depenses[i], depenses[i+1]
        if y1 is not None and y2 is not None and y1 <= budget < y2:
            t = (budget - y1) / (y2 - y1)
            d1, d2 = semaines[i], semaines[i+1]
            depassement_x = d1 + timedelta(seconds=t * (d2 - d1).total_seconds())
            depassement_label = depassement_x.strftime("%A %d %B %Y")
            break

    # DataFrame
    df = pd.DataFrame({
        "Semaine": semaines,
        "Dépenses constatées": depenses_constatees_aligned,
        "Dépenses prédites": depenses_predites_aligned,
        "Dépenses": depenses
    })

    # Graphique
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Semaine"], y=df["Dépenses constatées"],
        mode="lines+markers", name="Dépenses constatées", line=dict(color="blue")
    ))

    fig.add_trace(go.Scatter(
        x=df["Semaine"], y=df["Dépenses prédites"],
        mode="lines+markers", name="Dépenses prédites", line=dict(color="orange", dash="dot")
    ))

    fig.add_trace(go.Scatter(
        x=[df["Semaine"].iloc[0], df["Semaine"].iloc[-1]],
        y=[budget, budget],
        mode="lines", name="Budget", line=dict(color="red", dash="dash")
    ))

    if depassement_x is not None:
        fig.add_trace(go.Scatter(
            x=[depassement_x], y=[budget],
            mode="markers+text",
            marker=dict(size=18, color="red", symbol="circle"),
            text=[depassement_label],
            textposition="bottom center",
            showlegend=False
        ))
        st.info(f"Le budget sera dépassé autour du {depassement_label}")

    fig.update_layout(
        title="Suivi des dépenses en août 2025",
        xaxis_title="Date",
        yaxis_title="Montant (€)",
        xaxis=dict(type="date"),
        legend=dict(x=0.02, y=0.98),
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    page_courbe()
