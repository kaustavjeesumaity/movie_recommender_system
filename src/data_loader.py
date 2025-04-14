import pandas as pd
import requests
import zipfile
from tqdm import tqdm
import os

class DataLoader:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
    
    def download_dataset(self, url, filename):
        """Download dataset from URL with progress bar"""
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'wb') as f, tqdm(
            desc=filename,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                bar.update(size)
        
        return filepath
    
    def extract_zip(self, zip_path, extract_to=None):
        """Extract zip file"""
        if extract_to is None:
            extract_to = self.data_dir
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        return extract_to
    
    def load_movies(self, path):
        """Load movies data"""
        return pd.read_csv(path)
    
    def load_ratings(self, path):
        """Load ratings data"""
        return pd.read_csv(path)
    
    def load_tags(self, path):
        """Load tags data if available"""
        try:
            return pd.read_csv(path)
        except FileNotFoundError:
            return None