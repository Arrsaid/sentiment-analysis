import streamlit as st
import requests
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

# ========== Configuration ==========
API_URL = "https://sentiment-analysis-dxbncea7bxd4bqa7.spaincentral-01.azurewebsites.net/predict"
INSTRUMENTATION_KEY = "e211eb4d-f2ba-4322-a2ba-3f32d6141362"

# ========== Logger Azure ==========
logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logger.addHandler(
        AzureLogHandler(connection_string=f"InstrumentationKey={INSTRUMENTATION_KEY}")
    )
    logger.setLevel(logging.INFO)

# ========== Configuration de la page ==========
st.set_page_config(
    page_title="Analyse de sentiment - Air Paradis",
    page_icon="✈️",
    layout="centered",
)

# ========== Initialisation des états Streamlit ==========
st.session_state.setdefault("prediction_faite", False)
st.session_state.setdefault("sentiment", "")
st.session_state.setdefault("confidence", 0.0)
st.session_state.setdefault("feedback", None)
st.session_state.setdefault("last_tweet", "")
st.session_state.setdefault("trace_envoyee", False)

# ========== Interface Utilisateur ==========
st.title("Analyse de sentiment des tweets")
st.subheader("Entrez un tweet pour prédire son sentiment :")

user_input = st.text_area(
    "💬 Tweet", placeholder="Exemple : I love flying with Air Paradis!"
)

# ========== Action : Prédire ==========
if st.button("Prédire le sentiment"):
    if not user_input.strip():
        st.warning("Veuillez entrer un tweet.")
    else:
        with st.spinner("Analyse en cours..."):
            try:
                response = requests.post(API_URL, json={"text": user_input})
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.sentiment = result["sentiment"]
                    st.session_state.confidence = result["confidence"] * 100
                    st.session_state.last_tweet = user_input
                    st.session_state.prediction_faite = True
                    st.session_state.feedback = None
                    st.session_state.trace_envoyee = False
                else:
                    st.error(f"Erreur de l'API : {response.status_code}")
            except requests.exceptions.RequestException:
                st.error("❌ Impossible de se connecter à l'API.")

# ========== Affichage des résultats ==========
if st.session_state.prediction_faite:
    sentiment = st.session_state.sentiment
    confidence = st.session_state.confidence

    if sentiment == "positif":
        st.success(f"✨ Sentiment prédit : **Positif** ({confidence:.2f}%)")
    else:
        st.error(f"⚠️ Sentiment prédit : **Négatif** ({confidence:.2f}%)")

    # Boutons de feedback
    st.markdown("##### Cette prédiction vous semble-t-elle correcte ?")
    st.markdown(" ")
    col1, col2 = st.columns(2)

    # Gestion du clic sur les boutons
    if col1.button("✅ Oui, c’est correct"):
        st.session_state.feedback = "yes"
    if col2.button("❌ Non, c’est incorrect"):
        st.session_state.feedback = "no"
        if not st.session_state.trace_envoyee:
            logger.warning(
                "Mauvaise prédiction détectée par l'utilisateur",
                extra={
                    "custom_dimensions": {
                        "tweet": st.session_state.last_tweet,
                        "sentiment_prevu": sentiment,
                        "confiance": confidence,
                    }
                },
            )
            st.session_state.trace_envoyee = True

    # Affichage du message de retour (plein écran)
    if st.session_state.feedback == "yes":
        st.info("✅ Merci pour votre confirmation.")
    elif st.session_state.feedback == "no":
        st.warning("⚠️ Merci pour votre retour. L'information a été transmise.")
