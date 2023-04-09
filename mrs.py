import pickle
import streamlit as st
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    movie_ratings = movie_sentiments[index]
    distances = []
    for i in range(len(movies)):
        sim = similarity[index][i]
        sentiment_sim = abs(movie_ratings - movie_sentiments[i])
        total_sim = sim + sentiment_sim
        distances.append((i, total_sim))
    distances = sorted(distances, reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return ( recommended_movie_names,recommended_movie_posters)

st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# Load user ratings and feedback
user_feedback = pickle.load(open('user_feedback.pkl','rb'))

# Perform sentiment analysis on the user feedback
analyzer = SentimentIntensityAnalyzer()
movie_sentiments = []
for feedback in user_feedback:
    sentiment = analyzer.polarity_scores(feedback)['compound']
    movie_sentiments.append(sentiment)

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
