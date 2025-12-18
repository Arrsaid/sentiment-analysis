import warnings
import pickle

from fastapi import FastAPI
from pydantic import BaseModel
from utils import preprocess_tweet

# Configuration
warnings.filterwarnings("ignore")

# Initialisation FastAPI
app = FastAPI(title="API- Analyse de sentiment")

# Variable globale
pipeline = None


# Chargement du pipeline au démarrage
@app.on_event("startup")
def load_model():
    global pipeline
    print("Chargement du modèle...")

    with open("mon_pipeline.pkl", "rb") as f:
        pipeline = pickle.load(f)

    print("Modèle chargé avec succès.")


# Modèle de requête
class Tweet(BaseModel):
    text: str


# Route de santé
@app.get("/")
def read_root():
    return {"message": "API de prédiction de sentiment - en ligne"}


# Route de prédiction
@app.post("/predict")
def predict(tweet: Tweet):
    # Nettoyage éventuel du texte
    cleaned = preprocess_tweet(tweet.text, rejoin=True)

    # Prédiction
    pred_class = pipeline.predict([cleaned])[0]
    proba = pipeline.predict_proba([cleaned])[0].max()

    sentiment = "positif" if pred_class == 1 else "négatif"
    confidence = round(float(proba), 4)

    return {"sentiment": sentiment, "confidence": confidence}
