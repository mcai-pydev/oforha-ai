"""
Customer Segmentation Template
A comprehensive customer segmentation system using clustering algorithms
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from pathlib import Path
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomerSegmentation:
    def __init__(
        self,
        data_path: str,
        n_clusters: int = 5,
        random_state: int = 42
    ):
        """
        Initialize the CustomerSegmentation system
        
        Args:
            data_path (str): Path to the customer data CSV file
            n_clusters (int): Number of clusters for clustering algorithms
            random_state (int): Random state for reproducibility
        """
        self.data_path = data_path
        self.n_clusters = n_clusters
        self.random_state = random_state
        
        # Initialize data and models
        self.load_data()
        self.initialize_models()
        
        # Store results
        self.clusters = {}
        self.metrics = {}

    def load_data(self) -> None:
        """Load and prepare the customer data"""
        try:
            self.data = pd.read_csv(self.data_path)
            logger.info(f"Successfully loaded data from {self.data_path}")
            
            # Prepare features
            self.prepare_features()
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def prepare_features(self) -> None:
        """Prepare features for clustering"""
        # Example feature columns (modify based on your dataset)
        feature_columns = [
            'age', 'income', 'spending_score', 'purchase_frequency',
            'avg_purchase_value', 'customer_lifetime_value'
        ]
        
        # Select features
        self.features = self.data[feature_columns]
        
        # Scale features
        self.scaler = StandardScaler()
        self.features_scaled = self.scaler.fit_transform(self.features)
        
        logger.info(f"Prepared {len(feature_columns)} features for clustering")

    def initialize_models(self) -> None:
        """Initialize clustering models"""
        try:
            # K-means
            self.models['kmeans'] = KMeans(
                n_clusters=self.n_clusters,
                random_state=self.random_state
            )
            
            # DBSCAN
            self.models['dbscan'] = DBSCAN(
                eps=0.5,
                min_samples=5
            )
            
            # Agglomerative Clustering
            self.models['hierarchical'] = AgglomerativeClustering(
                n_clusters=self.n_clusters
            )
            
            # Gaussian Mixture Model
            self.models['gmm'] = GaussianMixture(
                n_components=self.n_clusters,
                random_state=self.random_state
            )
            
            logger.info("Successfully initialized clustering models")
        except Exception as e:
            logger.error(f"Error initializing models: {str(e)}")
            raise

    def perform_clustering(self) -> None:
        """Perform clustering using all models"""
        try:
            for name, model in self.models.items():
                # Fit and predict
                if name == 'dbscan':
                    clusters = model.fit_predict(self.features_scaled)
                else:
                    clusters = model.fit_predict(self.features_scaled)
                
                # Store results
                self.clusters[name] = clusters
                
                # Calculate metrics
                if name != 'dbscan':  # DBSCAN doesn't support all metrics
                    self.metrics[name] = {
                        'silhouette': silhouette_score(self.features_scaled, clusters),
                        'calinski_harabasz': calinski_harabasz_score(self.features_scaled, clusters),
                        'davies_bouldin': davies_bouldin_score(self.features_scaled, clusters)
                    }
            
            logger.info("Successfully performed clustering with all models")
        except Exception as e:
            logger.error(f"Error performing clustering: {str(e)}")
            raise

    def analyze_clusters(self, model_name: str) -> Dict:
        """
        Analyze cluster characteristics
        
        Args:
            model_name (str): Name of the clustering model to analyze
            
        Returns:
            Dict: Dictionary containing cluster analysis results
        """
        try:
            if model_name not in self.clusters:
                raise ValueError(f"Model {model_name} not found")
            
            # Add cluster labels to original data
            self.data[f'cluster_{model_name}'] = self.clusters[model_name]
            
            # Calculate cluster statistics
            cluster_stats = {}
            for cluster in range(self.n_clusters):
                cluster_data = self.data[self.data[f'cluster_{model_name}'] == cluster]
                cluster_stats[f'cluster_{cluster}'] = {
                    'size': len(cluster_data),
                    'mean_values': cluster_data[self.features.columns].mean().to_dict(),
                    'std_values': cluster_data[self.features.columns].std().to_dict()
                }
            
            return cluster_stats
        except Exception as e:
            logger.error(f"Error analyzing clusters: {str(e)}")
            raise

    def plot_clusters(
        self,
        model_name: str,
        feature1: str,
        feature2: str,
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Plot clusters using two features
        
        Args:
            model_name (str): Name of the clustering model to plot
            feature1 (str): First feature to plot
            feature2 (str): Second feature to plot
            save_path (Optional[str]): Path to save the plot
            
        Returns:
            plt.Figure: Matplotlib figure object
        """
        try:
            if model_name not in self.clusters:
                raise ValueError(f"Model {model_name} not found")
            
            # Create scatter plot
            plt.figure(figsize=(10, 8))
            scatter = plt.scatter(
                self.data[feature1],
                self.data[feature2],
                c=self.clusters[model_name],
                cmap='viridis'
            )
            
            plt.title(f'Customer Clusters - {model_name.upper()}')
            plt.xlabel(feature1)
            plt.ylabel(feature2)
            plt.colorbar(scatter, label='Cluster')
            
            if save_path:
                plt.savefig(save_path)
            
            return plt.gcf()
        except Exception as e:
            logger.error(f"Error plotting clusters: {str(e)}")
            raise

    def get_cluster_profiles(self, model_name: str) -> Dict:
        """
        Generate detailed cluster profiles
        
        Args:
            model_name (str): Name of the clustering model to profile
            
        Returns:
            Dict: Dictionary containing cluster profiles
        """
        try:
            if model_name not in self.clusters:
                raise ValueError(f"Model {model_name} not found")
            
            profiles = {}
            for cluster in range(self.n_clusters):
                cluster_data = self.data[self.data[f'cluster_{model_name}'] == cluster]
                
                # Calculate profile characteristics
                profile = {
                    'size': len(cluster_data),
                    'percentage': len(cluster_data) / len(self.data) * 100,
                    'characteristics': {}
                }
                
                # Calculate characteristics for each feature
                for feature in self.features.columns:
                    profile['characteristics'][feature] = {
                        'mean': cluster_data[feature].mean(),
                        'median': cluster_data[feature].median(),
                        'std': cluster_data[feature].std(),
                        'min': cluster_data[feature].min(),
                        'max': cluster_data[feature].max()
                    }
                
                profiles[f'cluster_{cluster}'] = profile
            
            return profiles
        except Exception as e:
            logger.error(f"Error generating cluster profiles: {str(e)}")
            raise

def main():
    """Example usage of the CustomerSegmentation class"""
    try:
        # Example data path
        data_path = "customer_data.csv"
        
        # Initialize segmentation system
        segmentation = CustomerSegmentation(data_path)
        
        # Perform clustering
        segmentation.perform_clustering()
        
        # Analyze clusters
        for model_name in segmentation.models.keys():
            # Get cluster analysis
            analysis = segmentation.analyze_clusters(model_name)
            print(f"\nCluster Analysis for {model_name}:")
            print(json.dumps(analysis, indent=2))
            
            # Get cluster profiles
            profiles = segmentation.get_cluster_profiles(model_name)
            print(f"\nCluster Profiles for {model_name}:")
            print(json.dumps(profiles, indent=2))
            
            # Plot clusters
            fig = segmentation.plot_clusters(
                model_name,
                'income',
                'spending_score',
                f'clusters_{model_name}.png'
            )
            plt.close(fig)
        
        # Print clustering metrics
        print("\nClustering Metrics:")
        print(json.dumps(segmentation.metrics, indent=2))
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 