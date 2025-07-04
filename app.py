import pickle
import streamlit as st
import requests

import os
import gdown

def download_file(file_id, output_name):
    if not os.path.exists(output_name):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output_name, quiet=False)
        print(f"{output_name} downloaded.")

# Download required files from Google Drive
download_file("16ZTlZTJ5i7_y4fqn9xyZX0dEUpMmfFxo", "similarity.pkl")
download_file("1u3GAKoUw3vWlftK48Vp_chyUAMHHg5_2", "movie_list.pkl")


def fetch_movie_details(movie_id):
    # Get movie details
    details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    details_data = requests.get(details_url).json()

    # Get trailer video
    video_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    video_data = requests.get(video_url).json()

    # Default values
    poster_path = details_data.get('poster_path', '')
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ""
    overview = details_data.get('overview', 'No description available.')
    rating = details_data.get('vote_average', 'N/A')

    # Find YouTube trailer
    trailer_url = "Trailer not available"
    for video in video_data.get('results', []):
        if video['type'] == 'Trailer' and video['site'] == 'YouTube':
            trailer_url = f"https://www.youtube.com/watch?v={video['key']}"
            break

    return full_path, overview, rating, trailer_url


# --------------------------------------------
# Recommendation Function
# --------------------------------------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_overviews = []
    recommended_movie_ratings = []
    recommended_movie_trailers = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster, overview, rating, trailer_url = fetch_movie_details(movie_id)
        
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(poster)
        recommended_movie_overviews.append(overview)
        recommended_movie_ratings.append(rating)
        recommended_movie_trailers.append(trailer_url)

    return (recommended_movie_names, 
            recommended_movie_posters, 
            recommended_movie_overviews,
            recommended_movie_ratings,
            recommended_movie_trailers)

# --------------------------------------------
# Streamlit App UI
# --------------------------------------------

st.set_page_config(page_title="Movie Recommender", layout="wide")

# Sidebar info
st.sidebar.title("🎬 Movie Recommender")
st.sidebar.markdown("""
This app recommends movies based on your selection using content-based filtering.  
Data source: [TMDB](https://www.themoviedb.org/)

**Made by:** Ansh Viradiya  
""")

st.header('Movie Recommender System 🍿')

# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Dropdown movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Show Recommendations
if st.button('Show Recommendation'):
    names, posters, overviews, ratings, trailers = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.subheader(names[i])
            st.caption(f"⭐ IMDb Rating: {ratings[i]}")
            st.write(overviews[i][:150] + "...")
            st.markdown(f"[🎬 Watch Trailer]({trailers[i]})", unsafe_allow_html=True)

