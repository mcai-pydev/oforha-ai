"""
Data Analysis Tool Template
A comprehensive tool for data analysis and visualization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataAnalyzer:
    def __init__(self, data_path: str):
        """
        Initialize the DataAnalyzer with a data file path
        
        Args:
            data_path (str): Path to the data file (CSV, Excel, etc.)
        """
        self.data_path = data_path
        self.data = None
        self.load_data()

    def load_data(self) -> None:
        """Load data from the specified file"""
        try:
            if self.data_path.endswith('.csv'):
                self.data = pd.read_csv(self.data_path)
            elif self.data_path.endswith(('.xlsx', '.xls')):
                self.data = pd.read_excel(self.data_path)
            else:
                raise ValueError("Unsupported file format")
            logger.info(f"Successfully loaded data from {self.data_path}")
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def get_basic_stats(self) -> Dict:
        """
        Get basic statistical information about the dataset
        
        Returns:
            Dict: Dictionary containing basic statistics
        """
        stats = {
            'shape': self.data.shape,
            'columns': self.data.columns.tolist(),
            'missing_values': self.data.isnull().sum().to_dict(),
            'data_types': self.data.dtypes.to_dict(),
            'summary': self.data.describe().to_dict()
        }
        return stats

    def create_visualization(
        self,
        plot_type: str,
        x: str,
        y: Optional[str] = None,
        title: Optional[str] = None
    ) -> plt.Figure:
        """
        Create various types of visualizations
        
        Args:
            plot_type (str): Type of plot ('bar', 'line', 'scatter', 'histogram')
            x (str): Column name for x-axis
            y (str, optional): Column name for y-axis
            title (str, optional): Plot title
            
        Returns:
            plt.Figure: Matplotlib figure object
        """
        plt.figure(figsize=(10, 6))
        
        if plot_type == 'bar':
            self.data[x].value_counts().plot(kind='bar')
        elif plot_type == 'line':
            self.data.plot(x=x, y=y, kind='line')
        elif plot_type == 'scatter':
            self.data.plot(x=x, y=y, kind='scatter')
        elif plot_type == 'histogram':
            self.data[x].hist()
        else:
            raise ValueError(f"Unsupported plot type: {plot_type}")
            
        plt.title(title or f"{plot_type.capitalize()} Plot")
        plt.tight_layout()
        return plt.gcf()

    def analyze_correlations(self) -> pd.DataFrame:
        """
        Analyze correlations between numeric columns
        
        Returns:
            pd.DataFrame: Correlation matrix
        """
        numeric_data = self.data.select_dtypes(include=[np.number])
        return numeric_data.corr()

    def handle_missing_values(self, method: str = 'mean') -> None:
        """
        Handle missing values in the dataset
        
        Args:
            method (str): Method to handle missing values ('mean', 'median', 'mode', 'drop')
        """
        if method == 'mean':
            self.data.fillna(self.data.mean(), inplace=True)
        elif method == 'median':
            self.data.fillna(self.data.median(), inplace=True)
        elif method == 'mode':
            self.data.fillna(self.data.mode().iloc[0], inplace=True)
        elif method == 'drop':
            self.data.dropna(inplace=True)
        else:
            raise ValueError(f"Unsupported method: {method}")

def main():
    """Example usage of the DataAnalyzer class"""
    # Example data path
    data_path = "sample_data.csv"
    
    try:
        # Initialize analyzer
        analyzer = DataAnalyzer(data_path)
        
        # Get basic statistics
        stats = analyzer.get_basic_stats()
        print("Basic Statistics:", stats)
        
        # Create visualizations
        fig1 = analyzer.create_visualization(
            plot_type='bar',
            x='category',
            title='Category Distribution'
        )
        fig1.savefig('category_distribution.png')
        
        # Analyze correlations
        correlations = analyzer.analyze_correlations()
        print("Correlations:", correlations)
        
        # Handle missing values
        analyzer.handle_missing_values(method='mean')
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 