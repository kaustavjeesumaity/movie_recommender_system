# main.py
from src.data_loader import DataLoader
from src.data_analyzer import DataAnalyzer
from src.recommender import MovieRecommender
from src.report_generator import ReportGenerator

def main():
    # Initialize components
    loader = DataLoader()
    
    # Load data
    movies = loader.load_movies("data/ml-latest-small/movies.csv")
    ratings = loader.load_ratings("data/ml-latest-small/ratings.csv")
    
    # Analyze data
    analyzer = DataAnalyzer(movies, ratings)
    stats = analyzer.basic_stats()
    top_movies = analyzer.get_top_movies()
    
    # Generate recommendations
    recommender = MovieRecommender(movies, ratings)
    recommendations = recommender.recommend_similar_movies("Toy Story (1995)")
    
    # Generate and save report
    report_path = ReportGenerator.generate_movie_report(
        movies=movies,
        ratings=ratings,
        stats=stats,
        top_movies=top_movies,
        recommendations=recommendations
    )
    
    print(f"Successfully generated report: {report_path}")

if __name__ == "__main__":
    main()