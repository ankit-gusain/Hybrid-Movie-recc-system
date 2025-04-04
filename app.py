import streamlit as st
import requests
import pandas as pd

# TMDB API Key (Replace with your API key)
TMDB_API_KEY = "e22def756578a3a85977d58ef5b38d0a"

# Function to fetch movie poster from TMDB
def get_movie_poster(movie_title):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
    response = requests.get(search_url)
    if response.status_code == 200 and response.json()["results"]:
        poster_path = response.json()["results"][0].get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/150"  # Default placeholder if not found

# Set up Streamlit page config
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# Page Header
st.title("🎬 Movie Recommendation System")
st.markdown("🔍 Get personalized movie recommendations based on your preferences!")

# Sidebar Inputs
st.sidebar.header("⚙️ Configure Your Preferences")
user_id = st.sidebar.number_input("Enter User ID:", min_value=1, step=1, value=1)
genre = st.sidebar.text_input("Enter Genre (Optional):")
filter_type = st.sidebar.selectbox("Select Filter Type:", ["popular", "trending", "None"], index=0)
top_n = st.sidebar.slider("Number of Recommendations:", min_value=1, max_value=10, value=5)

# API base URL (Replace with your actual localhost/ngrok URL)
BASE_URL = "https://9175-35-196-177-83.ngrok-free.app/recommend"

# Main content area with tabs
tab1, tab2 = st.tabs(["📢 Recommendations", "ℹ️ About"])

with tab1:
    if st.button("🎥 Get Recommendations"):
        with st.spinner("🔄 Fetching movie recommendations..."):
            params = {
                "user_id": user_id,
                "genre": genre if genre else "",
                "filter_type": filter_type if filter_type != "None" else "",
                "top_n": top_n
            }
            
            response = requests.get(BASE_URL, params=params)
            
            if response.status_code == 200:
                recommendations = response.json()

                if "error" in recommendations or not recommendations:
                    st.error("⚠️ No recommendations found. Try different settings!")
                else:
                    df = pd.DataFrame(recommendations)
                    st.success(f"✅ Found {len(df)} movies for you!")

                    # Display movies with posters (if available)
                    for _, row in df.iterrows():
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            # Fetch poster using TMDB
                            poster_url = get_movie_poster(row['title'])
                            st.image(poster_url, width=120)
                        with col2:
                            st.markdown(f"**🎬 {row['title']}**")
                            st.markdown(f"📅 Release Date: {row['release_date']}")
                            st.markdown(f"⭐ Rating: {row['vote_average']} / 10")
                            st.markdown(f"🎭 Genres: {', '.join(row['genres'])}")
                            st.write("---")
            else:
                st.error("❌ Failed to fetch recommendations. Check API URL and try again!")

with tab2:
    st.markdown("### ℹ️ About This App")
    st.write("This Movie Recommendation System uses a hybrid approach, combining collaborative filtering with content-based filtering. It suggests trending and popular movies based on user preferences.")
    st.write("📌 **Technologies Used:**")
    st.markdown("- 🎯 LightFM for collaborative filtering")
    st.markdown("- 🏆 Popularity & trending scores for recommendations")
    st.markdown("- 🎭 Genre & actor-based filtering")
    st.write("**Developed by:**Ankit🚀")
