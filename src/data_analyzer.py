import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalyzer:
    def __init__(self, movies, ratings, tags=None):
        self.movies = movies
        self.ratings = ratings
        self.tags = tags
    
    def basic_stats(self):
        """Return statistics as a dictionary of DataFrames"""
        stats = {}
        
        # Movies stats
        stats['movies'] = pd.DataFrame({
            'Total Movies': [len(self.movies)],
            'Unique Genres': [len(self.movies['genres'].str.split('|').explode().unique())]
        })
        
        # Ratings stats
        stats['ratings'] = self.ratings['rating'].describe().to_frame('Value')
        
        # Ratings per movie
        ratings_per_movie = self.ratings.groupby('movieId').size()
        stats['ratings_per_movie'] = ratings_per_movie.describe().to_frame('Value')
        
        return stats
    
    def plot_rating_distribution(self):
        """Plot distribution of ratings"""
        plt.figure(figsize=(10, 6))
        sns.countplot(x='rating', data=self.ratings)
        plt.title('Distribution of Ratings')
        return plt
    
    def get_top_movies(self, min_votes=10, n=10):
        """Get top rated movies with minimum votes as DataFrame"""
        movie_stats = self.ratings.groupby('movieId').agg(
            avg_rating=('rating', 'mean'),
            num_ratings=('rating', 'count')
        ).join(self.movies.set_index('movieId'))
        
        top_movies = movie_stats[movie_stats['num_ratings'] >= min_votes]\
            .sort_values('avg_rating', ascending=False)\
            .head(n)
        
        return top_movies[['title', 'genres', 'avg_rating', 'num_ratings']].reset_index(drop=True)