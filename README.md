# 🎬 Movie Recommender System

This is a web-based Movie Recommender App built using Streamlit. It uses content-based filtering with scikit-learn to suggest similar movies. The app fetches real-time posters, overviews, IMDb ratings, and official trailers using the TMDB API.

## 🎥 Demo

👉 Live App: https://movie-recommender-system-3mzxwibphl8tauuravu7kf.streamlit.app/

## 🛠️ Tech Stack

- Python
- Pandas, NumPy
- Scikit-learn
- NLTK / SpaCy (optional for NLP)
- Streamlit
- Cosine Similarity
- TF-IDF Vectorizer

## ✨ Features

- Recommends top 5 similar movies
- Accepts movie name input from the user
- Displays posters and metadata of recommended movies
- Based on content similarity (not collaborative filtering)
- Clean and responsive Streamlit UI

## ⚙️ How It Works

1. Load the movie dataset (TMDB or Kaggle movies dataset).
2. Combine key features: genres, keywords, cast, crew, overview.
3. Preprocess text and create a single metadata column.
4. Apply TF-IDF Vectorizer to convert text to numerical vectors.
5. Use Cosine Similarity to find closest matches.
6. Display top 5 most similar movies with posters.

## 🧩 Installation

```bash
git clone https://github.com/anshhuuu/movie-recommendation-system.git
cd movie-recommendation-system
pip install -r requirements.txt
