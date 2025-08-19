import os
import streamlit as st
import requests

INGESTION_SERVICE_URL = os.environ["INGESTION_SERVICE_URL"]

def page_upload():
    client_id = 255

    # On utilise session_state pour garder le message après l'upload
    if "upload_result" not in st.session_state:
        st.session_state.upload_result = None

    st.header("Upload d'un ticket de caisse")

    # Si pas encore d'upload, on affiche l'uploader
    if st.session_state.upload_result is None:
        uploaded_file = st.file_uploader(
            "Choisissez une image de ticket de caisse",
            type=["png", "jpg", "jpeg"]
        )
        if uploaded_file is not None:
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            response = requests.post(
                f"{INGESTION_SERVICE_URL}/clients/{client_id}/tickets", files=files
            )
            if response.status_code == 200:
                st.session_state.upload_result = ("success", "Image uploadée avec succès!")
            else:
                st.session_state.upload_result = ("error", f"Erreur lors de l'upload: {response.status_code}")
            st.rerun()
    else:
        # Affiche le message (succès ou erreur) et propose de réinitialiser
        status, msg = st.session_state.upload_result
        if status == "success":
            st.success(msg)
        else:
            st.error(msg)
        if st.button("Uploader une autre image"):
            st.session_state.upload_result = None
            st.rerun()