import streamlit as st
import requests
import plotly.graph_objs as go

def page_courbe():
    st.header("Affichage de la courbe")
    if st.button("Charger et afficher la courbe"):
        response = requests.get("https://xxx.com/zzz")
        if response.status_code == 200:
            data = response.json()
            x, y = data.get("x", []), data.get("y", [])
            fig = go.Figure(data=go.Scatter(x=x, y=y, mode="lines+markers"))
            fig.update_layout(title="Courbe depuis JSON")
            st.plotly_chart(fig)
        else:
            st.error("Impossible de charger le JSON")