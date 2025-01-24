import streamlit as st
import pickle
import pandas as pd
import requests


# Function to fetch the movie poster using TMDb API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path', '')  # Use `.get()` to avoid KeyError
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Image+Available"  # Placeholder for missing posters


# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id  # Ensure `movie_id` exists in your DataFrame
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


# Load movies data and similarity matrix
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))  # Ensure the similarity file is correct

# Streamlit app title
st.title('Movie Recommender System')

# Dropdown to select a movie
selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)

# Recommend button functionality
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

    # Create columns to display recommendations
    cols = st.columns(5)  # Dynamically create 5 columns
    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.text(name)
            st.image(poster)
