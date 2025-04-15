from flask import Flask, render_template, request
from src.recommender import MovieRecommender
from src.data_loader import DataLoader
import requests
import os

app = Flask(__name__, static_url_path='/static')

# TMDB Configuration
TMDB_API_KEY = '9a45a8a1923b67bb0e9fc1c74d5f545a'
TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w200'  # w200 for thumbnail size

def get_movie_poster(tmdb_id):
    """Fetch movie poster from TMDB using tmdbId"""
    try:
        if not tmdb_id or str(tmdb_id) == 'nan':
            return None
            
        # Fetch movie details directly by ID
        url = f"https://api.themoviedb.org/3/movie/{int(tmdb_id)}?api_key={TMDB_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if data.get('poster_path'):
            return f"{TMDB_IMAGE_BASE_URL}{data['poster_path']}"
    except Exception as e:
        print(f"Error fetching poster for TMDB ID {tmdb_id}: {e}")
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    selected_movie = ""
    
    if request.method == 'POST':
        selected_movie = request.form['movie']
        if selected_movie:
            recommendations_df = recommender.recommend_similar_movies(selected_movie)
            recommendations = []
            for _, row in recommendations_df.iterrows():
                tmdb_id = links_df.loc[links_df['movieId'] == row['movieId'], 'tmdbId'].values[0]
                poster_url = get_movie_poster(tmdb_id)
                recommendations.append({
                    'title': row['title'],
                    'genres': row['genres'],
                    'poster_url': poster_url or '',
                    'tmdb_id': tmdb_id
                })
    
    movie_list = movies['title'].unique().tolist()
    return render_template('index.html',
                         movies=movie_list,
                         recommendations=recommendations,
                         selected_movie=selected_movie)

if __name__ == '__main__':
    # Load all data
    loader = DataLoader()
    movies = loader.load_movies("data/ml-latest-small/movies.csv")
    ratings = loader.load_ratings("data/ml-latest-small/ratings.csv")
    links_df = loader.load_links("data/ml-latest-small/links.csv")  # Make sure this method exists
    recommender = MovieRecommender(movies, ratings)
    
    # Create default poster if it doesn't exist
    os.makedirs('static/images', exist_ok=True)
    if not os.path.exists('static/images/default_poster.jpg'):
        # You should add a default poster image here
        pass
        
    app.run(debug=True)