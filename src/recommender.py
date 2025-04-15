import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class MovieRecommender:
    def __init__(self, movies, ratings):
        self.movies = movies
        self.ratings = ratings
        self.similarity_matrix = None
    
    def prepare_data(self):
        """Prepare data for recommendation"""
        self.movies['genres_clean'] = self.movies['genres'].str.replace('|', ' ')
    
    def build_similarity_matrix(self):
        """Build cosine similarity matrix based on genres"""
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(self.movies['genres_clean'])
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    def recommend_similar_movies(self, movie_title, n=5):
        """Recommend similar movies based on genre similarity as DataFrame"""
        if self.similarity_matrix is None:
            self.prepare_data()
            self.build_similarity_matrix()
        
        try:
            idx = self.movies[self.movies['title'] == movie_title].index[0]
        except IndexError:
            return pd.DataFrame(columns=['title', 'genres'])
        
        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:n+1]
        movie_indices = [i[0] for i in sim_scores]
        
        return self.movies.iloc[movie_indices][['movieId','title', 'genres']].reset_index(drop=True)