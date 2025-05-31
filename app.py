import streamlit as st
import requests

st.set_page_config(page_title="🎬 MovieVerse", layout="wide")

# Session state
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None
if "search_clicked" not in st.session_state:
    st.session_state.search_clicked = False

# Navigation function
def go_to_main():
    st.session_state.page = "main"

# Helper functions
def get_movie_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key=e22def756578a3a85977d58ef5b38d0a&query={movie_title}"
    res = requests.get(url)
    if res.status_code == 200 and res.json()["results"]:
        poster = res.json()["results"][0].get("poster_path")
        return f"https://image.tmdb.org/t/p/w500{poster}" if poster else "https://via.placeholder.com/150"
    return "https://via.placeholder.com/150"

def get_movie_trailer(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key=e22def756578a3a85977d58ef5b38d0a&query={movie_title}"
    res = requests.get(url)
    if res.status_code == 200 and res.json()["results"]:
        movie_id = res.json()["results"][0].get("id")
        if movie_id:
            video_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=e22def756578a3a85977d58ef5b38d0a"
            video_res = requests.get(video_url)
            if video_res.status_code == 200 and video_res.json()["results"]:
                for vid in video_res.json()["results"]:
                    if vid["type"].lower() == "trailer" and vid["site"].lower() == "youtube":
                        return f"https://www.youtube.com/embed/{vid['key']}"
    return None

def get_movie_details(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key=e22def756578a3a85977d58ef5b38d0a&query={movie_title}"
    res = requests.get(url)
    if res.status_code == 200 and res.json()["results"]:
        movie_id = res.json()["results"][0].get("id")
        if movie_id:
            det_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=e22def756578a3a85977d58ef5b38d0a&append_to_response=credits,genres"
            det_res = requests.get(det_url)
            return det_res.json() if det_res.status_code == 200 else None
    return None

# CSS
st.markdown("""
<style>
body {
    background-color: #141414;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}
.landing-wrapper {
    height: 90vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}
.landing-wrapper h1 {
    font-size: 3em;
    color: #E50914;
}
.landing-wrapper p {
    font-size: 1.2em;
    max-width: 600px;
}
.landing-wrapper img {
    width: 250px; /* Smaller size for the image */
    margin-bottom: 30px;
}
.start-button {
    padding: 12px 30px;
    font-size: 20px;
    background-color: #E50914;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}
.start-button:hover {
    background-color: #b00610;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.block-container {padding-top: 20px; padding-bottom: 0;}
</style>
""", unsafe_allow_html=True)

# === LANDING PAGE ===
if st.session_state.page == "landing":
    st.markdown("""
    <div class="landing-wrapper">
        <h1>Welcome to MovieVerse</h1>
        <p>Discover your next favorite movie. Choose your preferences and explore personalized recommendations powered by MovieVerse.</p> 
    </div>
    """, unsafe_allow_html=True)

    if st.button("Start Exploring", key="start-explore"):
        go_to_main()
    st.stop()

# === MAIN UI ===
st.markdown("<h1 style='color:#E50914;'>🎬 MovieVerse</h1>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h3 style='color: #E50914;'>Find Your Next Watch</h3>", unsafe_allow_html=True)
    user_id = st.number_input("User ID", min_value=1, step=1, value=1)
    genre = st.selectbox("Genre", ["All", "Action", "Comedy", "Drama", "Horror", "Sci-Fi","Thriller", "Romance", "Fantasy"])
    genre = "" if genre == "All" else genre
    filter_type = st.selectbox("Sort By", ["Popular", "Trending", "Top Rated"])
    top_n = st.slider("Number of Recommendations", 5, 20, 10)
    if st.button("🔍 Find Movies"):
        st.session_state.search_clicked = True

# Main movie display
if st.session_state.selected_movie is None:
    if not st.session_state.search_clicked:
        st.subheader("Use the sidebar to start discovering great movies!")
    else:
        try:
            BASE_URL = "https://832e-104-197-119-194.ngrok-free.app/recommend"
            params = { 
                "user_id": user_id,
                "genre": genre,
                "filter_type": filter_type.lower() if filter_type != "Top Rated" else "top_rated",
                "top_n": top_n
            }
            res = requests.get(BASE_URL, params=params)
            if res.status_code == 200 and res.json():
                movies = res.json()
                st.subheader("🎥 Recommended Movies")
                for i, movie in enumerate(movies):
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        # Use container width for image to avoid deprecation warning
                        st.image(movie.get("poster_path", get_movie_poster(movie["title"])), use_container_width=True, width=700)
                    with col2:
                        st.markdown(f"**{movie['title']}**", unsafe_allow_html=True)
                        st.markdown(f"⭐ {movie.get('vote_average', 'N/A')}/10", unsafe_allow_html=True)
                        
                        # Add proper spacing before the "View Details" button
                        st.markdown("<br><br>", unsafe_allow_html=True)
                        
                        if st.button("Details", key=f"details_{i}"):
                            st.session_state.selected_movie = movie
                            st.rerun()
            else:
                st.warning("No recommendations found. Try different settings.")
        except Exception as e:
            st.error(f"Error fetching recommendations: {e}")
else:
    movie = st.session_state.selected_movie
    details = get_movie_details(movie["title"]) or {}
    trailer_url = get_movie_trailer(movie["title"])
    
    # Displaying the movie title and additional information
    st.markdown(f"**🎬 {movie['title']}**")
    st.markdown(f"📅 Release Date: {movie.get('release_date', 'N/A')}")
    st.markdown(f"⭐ Rating: {movie.get('vote_average', 'N/A')} / 10")
    st.markdown(f"🎭 Genres: {', '.join([genre['name'] for genre in details.get('genres', [])])}")
    st.write("---")
    
    # Movie Overview
    st.markdown(f"## Overview:")
    st.write(details.get("overview", "No overview available."))
    
    # Display movie poster and trailer
    st.image(movie.get("poster_path", get_movie_poster(movie["title"])), use_container_width=True, width=700)
    
    # Display trailer if available
    if trailer_url:
        st.video(trailer_url)
    
    # Back button
    if st.button("🔙 Back to Results"):
        st.session_state.selected_movie = None
        st.rerun()
