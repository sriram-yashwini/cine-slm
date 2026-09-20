import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Safely retrieve key from Streamlit Secrets or local .env
OMDB_API_KEY = None
try:
    if "OMDB_API_KEY" in st.secrets:
        OMDB_API_KEY = str(st.secrets["OMDB_API_KEY"]).strip()
except Exception:
    pass

if not OMDB_API_KEY:
    OMDB_API_KEY = os.getenv("OMDB_API_KEY", "").strip()

BASE_URL = "https://www.omdbapi.com/"


def search_movie(movie_name):
    """
    Search for movies by name safely without crashing the Streamlit UI.
    """
    if not OMDB_API_KEY or OMDB_API_KEY == "your_actual_omdb_key":
        st.error("Missing or invalid OMDb API Key. Please add OMDB_API_KEY in Streamlit App Settings -> Secrets.")
        return []

    params = {
        "apikey": OMDB_API_KEY,
        "s": movie_name,
        "type": "movie"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=15)
        
        # Check HTTP status code manually before calling raise_for_status
        if response.status_code == 401:
            st.error("OMDb Error 401: Unauthorized. Your API key is invalid or not yet activated via email.")
            return []
        
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "False":
            st.warning(data.get("Error", "No movies found."))
            return []

        return data.get("Search", [])

    except requests.exceptions.RequestException as err:
        st.error(f"Network / API Error: {err}")
        return []


def get_movie_details(imdb_id):
    """
    Get complete movie details using IMDb ID.
    """
    if not OMDB_API_KEY or OMDB_API_KEY == "your_actual_omdb_key":
        return None

    params = {
        "apikey": OMDB_API_KEY,
        "i": imdb_id,
        "plot": "full"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=15)
        if response.status_code != 200:
            return None

        data = response.json()
        if data.get("Response") == "False":
            return None

        return data
    except Exception:
        return None