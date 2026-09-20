# Movie Information Assistant

## Project Description

Movie Information Assistant is a Streamlit-based application that allows users
to search for movies and view detailed movie information.

The application uses the OMDb API to retrieve movie information such as:

- Movie title
- Release year
- Genre
- Director
- Actors
- Runtime
- IMDb rating
- Language
- Country
- Awards
- Story/Plot
- Ratings

## Technologies Used

- Python
- Streamlit
- OMDb API
- Requests
- python-dotenv

## Project Structure

Movie_SLM/
│
├── src/
│   └── omdb.py
│
├── app.py
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore

## Setup Instructions

### 1. Create virtual environment

python -m venv movie_env

### 2. Activate virtual environment

.\movie_env\Scripts\Activate.ps1

### 3. Install dependencies

pip install -r requirements.txt

### 4. Configure OMDb API Key

Create a .env file in the project folder.

Add:

OMDB_API_KEY=your_actual_api_key

### 5. Run the application

python -m streamlit run app.py

## Application Flow

User enters movie name
        ↓
OMDb API search
        ↓
Matching movies displayed
        ↓
User selects a movie
        ↓
Movie details retrieved using IMDb ID
        ↓
Movie information displayed in Streamlit

