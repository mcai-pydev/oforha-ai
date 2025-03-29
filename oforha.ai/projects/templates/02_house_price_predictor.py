"""
House Price Predictor Template
A machine learning model to predict house prices
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HousePricePredictor:
    def __init__(self, data_path: str):
        """
        Initialize the HousePricePredictor with a data file path
        
        Args:
            data_path (str): Path to the house price dataset
        """
        self.data_path = data_path
        self.data = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.models = {}
        self.load_data()

    def load_data(self) -> None:
        """Load and prepare the house price dataset"""
        try:
            self.data = pd.read_csv(self.data_path)
            logger.info(f"Successfully loaded data from {self.data_path}")
            
            # Prepare features and target
            self.prepare_data()
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def prepare_data(self) -> None:
        """Prepare features and target variables"""
        # Example feature columns (modify based on your dataset)
        feature_columns = [
            'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot',
            'floors', 'waterfront', 'view', 'condition', 'grade',
            'sqft_above', 'sqft_basement', 'yr_built', 'yr_renovated',
            'zipcode', 'lat', 'long', 'sqft_living15', 'sqft_lot15'
        ]
        
        # Handle missing values
        self.data = self.data.fillna(self.data.mean())
        
        # Prepare features and target
        self.X = self.data[feature_columns]
        self.y = self.data['price']

    def split_data(self, test_size: float = 0.2) -> None:
        """
        Split data into training and testing sets
        
        Args:
            test_size (float): Proportion of data to use for testing
        """
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=42
        )
        
        # Scale features
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)

    def train_models(self) -> None:
        """Train multiple regression models"""
        # Linear Regression
        self.models['linear'] = LinearRegression()
        self.models['linear'].fit(self.X_train_scaled, self.y_train)
        
        # Ridge Regression
        self.models['ridge'] = Ridge(alpha=1.0)
        self.models['ridge'].fit(self.X_train_scaled, self.y_train)
        
        # Lasso Regression
        self.models['lasso'] = Lasso(alpha=1.0)
        self.models['lasso'].fit(self.X_train_scaled, self.y_train)
        
        # Random Forest
        self.models['rf'] = RandomForestRegressor(n_estimators=100, random_state=42)
        self.models['rf'].fit(self.X_train_scaled, self.y_train)

    def evaluate_models(self) -> Dict[str, Dict[str, float]]:
        """
        Evaluate all trained models
        
        Returns:
            Dict: Dictionary containing evaluation metrics for each model
        """
        results = {}
        
        for name, model in self.models.items():
            # Make predictions
            y_pred = model.predict(self.X_test_scaled)
            
            # Calculate metrics
            mse = mean_squared_error(self.y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(self.y_test, y_pred)
            
            results[name] = {
                'MSE': mse,
                'RMSE': rmse,
                'R2': r2
            }
        
        return results

    def plot_feature_importance(self, model_name: str = 'rf') -> plt.Figure:
        """
        Plot feature importance for the specified model
        
        Args:
            model_name (str): Name of the model to use
            
        Returns:
            plt.Figure: Matplotlib figure object
        """
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
            
        model = self.models[model_name]
        
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importances = np.abs(model.coef_)
        else:
            raise ValueError(f"Model {model_name} does not support feature importance")
            
        # Create feature importance plot
        plt.figure(figsize=(12, 6))
        importance_df = pd.DataFrame({
            'feature': self.X.columns,
            'importance': importances
        })
        importance_df = importance_df.sort_values('importance', ascending=False)
        
        sns.barplot(x='importance', y='feature', data=importance_df)
        plt.title(f'Feature Importance - {model_name.upper()}')
        plt.tight_layout()
        
        return plt.gcf()

    def predict_price(self, features: Dict[str, float]) -> float:
        """
        Predict house price for given features
        
        Args:
            features (Dict): Dictionary of feature values
            
        Returns:
            float: Predicted house price
        """
        # Convert features to DataFrame
        feature_df = pd.DataFrame([features])
        
        # Scale features
        feature_scaled = self.scaler.transform(feature_df)
        
        # Make prediction using best model
        best_model = self.models['rf']  # Using Random Forest as default
        prediction = best_model.predict(feature_scaled)[0]
        
        return prediction

def main():
    """Example usage of the HousePricePredictor class"""
    # Example data path
    data_path = "house_prices.csv"
    
    try:
        # Initialize predictor
        predictor = HousePricePredictor(data_path)
        
        # Split data
        predictor.split_data()
        
        # Train models
        predictor.train_models()
        
        # Evaluate models
        results = predictor.evaluate_models()
        print("Model Evaluation Results:", results)
        
        # Plot feature importance
        fig = predictor.plot_feature_importance()
        fig.savefig('feature_importance.png')
        
        # Example prediction
        sample_features = {
            'bedrooms': 3,
            'bathrooms': 2,
            'sqft_living': 2000,
            'sqft_lot': 5000,
            'floors': 1,
            'waterfront': 0,
            'view': 0,
            'condition': 3,
            'grade': 7,
            'sqft_above': 2000,
            'sqft_basement': 0,
            'yr_built': 2000,
            'yr_renovated': 0,
            'zipcode': 98122,
            'lat': 47.6062,
            'long': -122.3321,
            'sqft_living15': 2000,
            'sqft_lot15': 5000
        }
        
        predicted_price = predictor.predict_price(sample_features)
        print(f"Predicted House Price: ${predicted_price:,.2f}")
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 