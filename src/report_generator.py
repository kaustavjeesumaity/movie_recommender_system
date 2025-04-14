# src/report_generator.py
import pandas as pd
from datetime import datetime

class ReportGenerator:
    @staticmethod
    def generate_movie_report(movies, ratings, stats, top_movies, recommendations, filename=None):
        """
        Generate an Excel report with multiple sheets containing movie data analysis
        
        Args:
            movies (pd.DataFrame): Movies dataset
            ratings (pd.DataFrame): Ratings dataset
            stats (dict): Dictionary of statistics DataFrames
            top_movies (pd.DataFrame): Top rated movies
            recommendations (pd.DataFrame): Movie recommendations
            filename (str, optional): Output filename. If None, generates timestamped name.
        
        Returns:
            str: Path to the generated report
        """
        if filename is None:
            filename = f"movie_recommendation_report_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Movies data sheet
            movies.to_excel(writer, sheet_name='Movies Data', index=False)
            
            # Ratings data sheet (sample to avoid huge file)
            ratings.sample(min(1000, len(ratings))).to_excel(writer, sheet_name='Ratings Sample', index=False)
            
            # Statistics sheets
            for stat_name, stat_df in stats.items():
                stat_df.to_excel(writer, sheet_name=f'Stats - {stat_name}')
            
            # Top movies sheet
            top_movies.to_excel(writer, sheet_name='Top Rated Movies', index=False)
            
            # Recommendations sheet
            recommendations.to_excel(writer, sheet_name='Recommendations', index=False)
            
            # Add timestamp and metadata
            metadata = pd.DataFrame({
                'Generated on': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                'Total Movies': [len(movies)],
                'Total Ratings': [len(ratings)]
            })
            metadata.to_excel(writer, sheet_name='Report Info', index=False)
        
        return filename