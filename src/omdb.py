import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

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
    if not OMDB_API_KEY or OMDB_API_KEY == "your_actual_omdb_key":
        st.error("Invalid or missing OMDb API Key. Please configure OMDB_API_KEY in Streamlit Secrets.")
        return []

    params = {
        "apikey": OMDB_API_KEY,
        "s": movie_name,
        "type": "movie"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "False":
            st.info(data.get("Error", "No movies found matching your query."))
            return []

        return data.get("Search", [])

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            st.error("OMDb API Error (401 Unauthorized): Verify your API key is correct and activated via the email link.")
        else:
            st.error(f"HTTP error occurred: {http_err}")
        return []
    except Exception as err:
        st.error(f"An unexpected error occurred: {err}")
        return []


def get_movie_details(imdb_id):
    """
    Get complete movie details using IMDb ID.
    """
    if not OMDB_API_KEY or OMDB_API_KEY == "your_actual_omdb_key":
        st.error("Invalid or missing OMDb API Key.")
        return None

    params = {
        "apikey": OMDB_API_KEY,
        "i": imdb_id,
        "plot": "full"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "False":
            return None

        return data
    except Exception as err:
        st.error(f"Failed to fetch movie details: {err}")
        return None