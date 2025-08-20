import streamlit as st
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta

def page_courbe():
    st.title("Dépenses et prévisions - Août 2025")

    semaines_str = [
        "2025-08-04",
        "2025-08-11",
        "2025-08-18",
        "2025-08-25",
        "2025-09-01",
    ]
    semaines = [datetime.strptime(d, "%Y-%m-%d") for d in semaines_str]
    depenses_constatees = [210, 320, 450, None, None]
    depenses_predites   = [None, None, 450, 520, 600]
    budget = 500

    depenses = []
    for c, p in zip(depenses_constatees, depenses_predites):
        depenses.append(c if c is not None else p)

    # Calcul de la date de dépassement (interpolation linéaire)
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

    df = pd.DataFrame({
        "Semaine": semaines,
        "Dépenses constatées": depenses_constatees,
        "Dépenses prédites": depenses_predites,
        "Dépenses": depenses
    })

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

    # Point de dépassement sur l'axe x (hors légende, avec date affichée à côté)
    if depassement_x is not None:
        fig.add_trace(go.Scatter(
            x=[depassement_x], y=[0],
            mode="markers+text",
            marker=dict(size=18, color="red", symbol="circle"),
            text=[depassement_label],
            textposition="bottom center",
            showlegend=False  # Retire ce point de la légende
        ))
        st.info(f"Le budget sera dépassé autour du {depassement_label}")

    # Axe x lisible
    tickvals = df["Semaine"].tolist()
    ticktext = [
        "Semaine du 4 août",
        "Semaine du 11 août",
        "Semaine du 18 août",
        "Semaine du 25 août",
        "Semaine du 1er sept."
    ]
    fig.update_layout(
        title="Suivi des dépenses en août 2025",
        xaxis_title="Date",
        yaxis_title="Montant (€)",
        xaxis=dict(
            tickmode="array",
            tickvals=tickvals,
            ticktext=ticktext,
            type="date"
        ),
        legend=dict(x=0.02, y=0.98),
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    page_courbe()