from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import requests

BOT_TOKEN = '7572727020:AAFoVQUaGfupKLTnPhzQEHTwXZCn3Ku1W1s'
RECOMMENDER_API = 'https://b0a3-35-243-206-156.ngrok-free.app/recommend'
TMDB_API_KEY = "e22def756578a3a85977d58ef5b38d0a"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# Start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🎬 Welcome to Movie Genie Bot!\n"
        "Type /recommend to get your movie list!"
    )

# Genre selection
def recommend(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🎭 Comedy", callback_data='comedy')],
        [InlineKeyboardButton("🎥 Action", callback_data='action')],
        [InlineKeyboardButton("🧙 Fantasy", callback_data='fantasy')],
        [InlineKeyboardButton("🔥 Trending", callback_data='trending')],
        [InlineKeyboardButton("🎬 Romance", callback_data='romance')],
        [InlineKeyboardButton("🎭 Drama", callback_data='drama')],
        [InlineKeyboardButton("👻 Horror", callback_data='horror')],
        [InlineKeyboardButton("👽 Sci-Fi", callback_data='sci-fi')],
        [InlineKeyboardButton("🕵️ Mystery", callback_data='mystery')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Select a genre or filter:", reply_markup=reply_markup)

# Handle genre button
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    genre = query.data
    user_id = query.from_user.id

    params = {
        'user_id': user_id,
        'genre': genre if genre != 'trending' else '',
        'filter_type': 'trending' if genre == 'trending' else 'popular',
        'top_n': 5
    }
    response = requests.get(RECOMMENDER_API, params=params).json()

    if "error" in response:
        query.edit_message_text("❌ No recommendations found.")
        return

    for movie in response:
        title = movie.get("title", "Unknown Title")
        overview = movie.get("overview", "No overview available")
        popularity = round(movie.get("popularity", 0), 2)
        tmdb_id = movie.get("id")

        # Get poster from TMDB
        poster_url = fetch_poster(tmdb_id)
        caption = f"🎬 *{title}*\n\n📝 {overview}\n🔥 *Popularity:* {popularity} M"

        if poster_url:
            query.message.reply_photo(photo=poster_url, caption=caption, parse_mode="Markdown")
        else:
            query.message.reply_text(caption, parse_mode="Markdown")

# TMDB poster fetch function
def fetch_poster(movie_id):
    tmdb_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    try:
        res = requests.get(tmdb_url).json()
        poster_path = res.get('poster_path')  
        
        if poster_path:
            return f"{TMDB_IMAGE_BASE}{poster_path}"
    except:
        pass
    return None

# Placeholder image command
def image(update: Update, context: CallbackContext):
    update.message.reply_text("🖼️ Image generation is coming soon! Stay tuned.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("recommend", recommend))
    dp.add_handler(CommandHandler("image", image))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    print("🤖 Bot is running...")
    updater.idle()

if __name__ == '__main__':
    main()

##################################################################################


import streamlit as st
from streamlit_lottie import st_lottie
import requests
import pandas as pd

# Load Lottie animation from URL
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Fetch movie poster from TMDB
def get_movie_poster(movie_title):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key=e22def756578a3a85977d58ef5b38d0a&query={movie_title}"
    response = requests.get(search_url)
    if response.status_code == 200 and response.json()["results"]:
        poster_path = response.json()["results"][0].get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return "https://via.placeholder.com/150"

# Session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "intro"

def go_to_main():
    st.session_state.page = "main"

def go_to_intro():
    st.session_state.page = "intro"

# Page configuration
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# Inject full screen starry & moon background
st.markdown("""
    <style>
    body {
        background: black !important;
        color: white;
    }

    /* Full screen starry background */
    .stars {
        position: fixed;
        width: 100vw;
        height: 100vh;
        background: #000 url('https://raw.githubusercontent.com/VincentGarreau/particles.js/master/demo/media/star.png') repeat;
        animation: moveStars 300s linear infinite;
        top: 0;
        left: 0;
        z-index: -2;
    }

    /* Moon graphic */
    .moon {
        position: fixed;
        top: 40px;
        right: 60px;
        width: 150px;
        height: 150px;
        background: url('https://upload.wikimedia.org/wikipedia/commons/e/e1/FullMoon2010.jpg') no-repeat center center;
        background-size: cover;
        border-radius: 50%;
        box-shadow: 0 0 60px 15px #fff;
        z-index: -1;
    }

    /* Star animation */
    @keyframes moveStars {
        from { background-position: 0 0; }
        to { background-position: -10000px 5000px; }
    }

    /* Center button */
    .center-btn {
        display: flex;
        justify-content: center;
        margin-top: 30px;
    }

    .enter-button {
        background-color: #ff4b4b;
        color: white;
        border: none;
        padding: 16px 40px;
        font-size: 20px;
        border-radius: 50px;
        box-shadow: 0 0 20px #ff4b4b;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
    }

    .enter-button:hover {
        background-color: #fff;
        color: #000;
        transform: scale(1.1);
        box-shadow: 0 0 30px #fff;
    }
    </style>
    <div class="stars"></div>
    <div class="moon"></div>
""", unsafe_allow_html=True)

# ======= INTRO PAGE =======
if st.session_state.page == "intro":
    st.markdown("<h1 style='text-align:center; font-size: 64px;'>🌌 MovieVerse</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size: 20px;'>Your personalized gateway to cinematic discovery. Dive in and find your next favorite movie! 🍿</p>", unsafe_allow_html=True)
    st.markdown('<div class="center-btn"><button class="enter-button" onclick="window.location.reload()">🚀 Enter App</button></div>', unsafe_allow_html=True)

    if st.button("🚀 Enter App"):
        go_to_main()

# ======= MAIN PAGE =======
elif st.session_state.page == "main":
    if st.button("⬅️ Back to Intro"):
        go_to_intro()

    st.title("🎬 Movie Recommendation System")
    st.markdown("🔍 Get personalized movie recommendations based on your preferences!")

    st.sidebar.header("⚙️ Configure Your Preferences")
    user_id = st.sidebar.number_input("Enter User ID:", min_value=1, step=1, value=1)
    genre = st.sidebar.text_input("Enter Genre (Optional):")
    filter_type = st.sidebar.selectbox("Select Filter Type:", ["popular", "trending", "None"], index=0)
    top_n = st.sidebar.slider("Number of Recommendations:", min_value=1, max_value=10, value=5)

    BASE_URL = "https://eb8b-34-125-241-81.ngrok-free.app/recommend"

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

                        for _, row in df.iterrows():
                            col1, col2 = st.columns([1, 4])
                            with col1:
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
        st.write("This Movie Recommendation System uses a hybrid approach, combining collaborative filtering with content-based filtering.")
        st.markdown("- 🎯 LightFM for collaborative filtering")
        st.markdown("- 🏆 Popularity & trending scores for recommendations")
        st.markdown("- 🎭 Genre & actor-based filtering")
        st.write("**Developed by:** Ankit 🚀")
