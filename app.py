import streamlit as st

from src.omdb import search_movie, get_movie_details


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Movie Information Assistant",
    page_icon="🎬",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }

    .movie-result {
        padding: 12px 15px;
        border-radius: 10px;
        background-color: #f5f7fa;
        margin-bottom: 8px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# INITIALIZE SESSION STATE
# =========================================================

if "movies" not in st.session_state:
    st.session_state.movies = []

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🎬 Movie Information Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Search for a movie and explore its complete information.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SEARCH FORM
# =========================================================

with st.form("movie_search_form"):

    movie_name = st.text_input(
        "🔎 Search Movie",
        placeholder="Enter movie name, e.g. Interstellar",
        label_visibility="visible"
    )

    search_button = st.form_submit_button(
        "🔍 Search"
    )


# =========================================================
# SEARCH MOVIE
# =========================================================

if search_button:

    if not movie_name.strip():

        st.warning("Please enter a movie name.")

        st.session_state.movies = []
        st.session_state.selected_movie = None

    else:

        with st.spinner("Searching movies..."):

            movies = search_movie(movie_name.strip())

        st.session_state.movies = movies
        st.session_state.selected_movie = None


# =========================================================
# DISPLAY SEARCH RESULTS
# =========================================================

if st.session_state.movies:

    st.markdown(
        '<div class="section-title">🎬 Search Results</div>',
        unsafe_allow_html=True
    )

    st.write(
        f"Found {len(st.session_state.movies)} movie(s). "
        "Select a movie below:"
    )


    # -----------------------------------------------------
    # Display every movie directly
    # -----------------------------------------------------

    for index, movie in enumerate(st.session_state.movies):

        title = movie.get("Title", "Unknown Title")
        year = movie.get("Year", "Unknown Year")

        button_text = f"🎬 {title}  ({year})"

        if st.button(
            button_text,
            key=f"movie_{index}",
            use_container_width=True
        ):

            st.session_state.selected_movie = movie


# =========================================================
# DISPLAY SELECTED MOVIE
# =========================================================

if st.session_state.selected_movie:

    selected_movie = st.session_state.selected_movie

    imdb_id = selected_movie.get("imdbID")


    # -----------------------------------------------------
    # Get complete movie information
    # -----------------------------------------------------

    with st.spinner("Loading movie details..."):

        movie = get_movie_details(imdb_id)


    if movie:

        st.divider()


        # =================================================
        # MOVIE HEADER
        # =================================================

        poster_col, info_col = st.columns(
            [1, 2]
        )


        # -------------------------------------------------
        # POSTER
        # -------------------------------------------------

        with poster_col:

            poster = movie.get("Poster")

            if poster and poster != "N/A":

                st.image(
                    poster,
                    width=300
                )


        # -------------------------------------------------
        # BASIC INFORMATION
        # -------------------------------------------------

        with info_col:

            st.header(
                movie.get(
                    "Title",
                    "Not available"
                )
            )

            st.write(
                f"📅 **Year:** "
                f"{movie.get('Year', 'Not available')}"
            )

            st.write(
                f"🎭 **Genre:** "
                f"{movie.get('Genre', 'Not available')}"
            )

            st.write(
                f"🎬 **Director:** "
                f"{movie.get('Director', 'Not available')}"
            )

            st.write(
                f"👥 **Actors:** "
                f"{movie.get('Actors', 'Not available')}"
            )

            st.write(
                f"⏱️ **Runtime:** "
                f"{movie.get('Runtime', 'Not available')}"
            )

            st.write(
                f"⭐ **IMDb Rating:** "
                f"{movie.get('imdbRating', 'Not available')}"
            )


        # =================================================
        # MOVIE DETAILS
        # =================================================

        st.markdown(
            '<div class="section-title">📋 Movie Details</div>',
            unsafe_allow_html=True
        )


        detail_col1, detail_col2 = st.columns(2)


        with detail_col1:

            st.write(
                f"**Released:** "
                f"{movie.get('Released', 'Not available')}"
            )

            st.write(
                f"**Language:** "
                f"{movie.get('Language', 'Not available')}"
            )

            st.write(
                f"**Country:** "
                f"{movie.get('Country', 'Not available')}"
            )

            st.write(
                f"**Rated:** "
                f"{movie.get('Rated', 'Not available')}"
            )


        with detail_col2:

            st.write(
                f"**Writer:** "
                f"{movie.get('Writer', 'Not available')}"
            )

            st.write(
                f"**Awards:** "
                f"{movie.get('Awards', 'Not available')}"
            )

            st.write(
                f"**IMDb Votes:** "
                f"{movie.get('imdbVotes', 'Not available')}"
            )

            st.write(
                f"**Metascore:** "
                f"{movie.get('Metascore', 'Not available')}"
            )


        # =================================================
        # STORY
        # =================================================

        st.markdown(
            '<div class="section-title">📖 Story</div>',
            unsafe_allow_html=True
        )

        st.write(
            movie.get(
                "Plot",
                "Not available"
            )
        )


        # =================================================
        # RATINGS
        # =================================================

        ratings = movie.get("Ratings", [])


        if ratings:

            st.markdown(
                '<div class="section-title">⭐ Ratings</div>',
                unsafe_allow_html=True
            )


            for rating in ratings:

                source = rating.get(
                    "Source",
                    "Unknown"
                )

                value = rating.get(
                    "Value",
                    "N/A"
                )

                st.write(
                    f"**{source}:** {value}"
                )