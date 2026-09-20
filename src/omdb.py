import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load variables from .env for local development
load_dotenv()

# Get API key from Streamlit Secrets when deployed.
# Fall back to .env when running locally.
try:
    OMDB_API_KEY = st.secrets["OMDB_API_KEY"]
except Exception:
    OMDB_API_KEY = os.getenv("OMDB_API_KEY")

BASE_URL = "https://www.omdbapi.com/"

def search_movie(movie_name):
    """
    Search for movies by name.
    Returns a list of matching movies.
    """

    params = {
        "apikey": OMDB_API_KEY,
        "s": movie_name,
        "type": "movie"
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    # OMDb returns Response=False when search fails
    if data.get("Response") == "False":
        return []

    return data.get("Search", [])


def get_movie_details(imdb_id):
    """
    Get complete movie details using IMDb ID.
    """

    params = {
        "apikey": OMDB_API_KEY,
        "i": imdb_id,
        "plot": "full"
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    if data.get("Response") == "False":
        return None

    return data