"""
End-to-End ML Pipeline Template
A comprehensive machine learning pipeline with data processing, model training, and deployment
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple, Any
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_networks import MLPClassifier
import optuna
import mlflow
from mlflow.tracking import MlflowClient
import joblib
import logging
from pathlib import Path
import json
import os
import yaml
import time
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLPipeline:
    def __init__(
        self,
        config_path: str = "config.yaml",
        experiment_name: str = "ml_pipeline",
        tracking_uri: str = "http://localhost:5000"
    ):
        """
        Initialize the ML Pipeline
        
        Args:
            config_path (str): Path to the configuration file
            experiment_name (str): Name of the MLflow experiment
            tracking_uri (str): MLflow tracking URI
        """
        self.config_path = config_path
        self.experiment_name = experiment_name
        self.tracking_uri = tracking_uri
        
        # Load configuration
        self.load_config()
        
        # Initialize MLflow
        self.initialize_mlflow()
        
        # Initialize components
        self.initialize_components()
        
        # Store results
        self.results = {}

    def load_config(self) -> None:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            logger.info(f"Successfully loaded configuration from {self.config_path}")
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            raise

    def initialize_mlflow(self) -> None:
        """Initialize MLflow tracking"""
        try:
            mlflow.set_tracking_uri(self.tracking_uri)
            mlflow.set_experiment(self.experiment_name)
            logger.info("Successfully initialized MLflow")
        except Exception as e:
            logger.error(f"Error initializing MLflow: {str(e)}")
            raise

    def initialize_components(self) -> None:
        """Initialize pipeline components"""
        try:
            # Initialize data processors
            self.scaler = StandardScaler()
            self.label_encoder = LabelEncoder()
            
            # Initialize models
            self.models = {
                'random_forest': RandomForestClassifier(),
                'gradient_boosting': GradientBoostingClassifier(),
                'logistic_regression': LogisticRegression(),
                'svm': SVC(),
                'neural_network': MLPClassifier()
            }
            
            logger.info("Successfully initialized pipeline components")
        except Exception as e:
            logger.error(f"Error initializing components: {str(e)}")
            raise

    def load_data(self, data_path: str) -> pd.DataFrame:
        """
        Load and prepare data
        
        Args:
            data_path (str): Path to the data file
            
        Returns:
            pd.DataFrame: Loaded and prepared data
        """
        try:
            # Load data
            data = pd.read_csv(data_path)
            
            # Basic data cleaning
            data = self.clean_data(data)
            
            logger.info(f"Successfully loaded data from {data_path}")
            return data
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the input data
        
        Args:
            data (pd.DataFrame): Input data
            
        Returns:
            pd.DataFrame: Cleaned data
        """
        try:
            # Remove duplicates
            data = data.drop_duplicates()
            
            # Handle missing values
            data = data.fillna(data.mean())
            
            # Remove outliers
            for column in data.select_dtypes(include=[np.number]).columns:
                Q1 = data[column].quantile(0.25)
                Q3 = data[column].quantile(0.75)
                IQR = Q3 - Q1
                data = data[
                    (data[column] >= Q1 - 1.5 * IQR) &
                    (data[column] <= Q3 + 1.5 * IQR)
                ]
            
            return data
        except Exception as e:
            logger.error(f"Error cleaning data: {str(e)}")
            raise

    def prepare_features(
        self,
        data: pd.DataFrame,
        target_column: str
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare features and target
        
        Args:
            data (pd.DataFrame): Input data
            target_column (str): Name of the target column
            
        Returns:
            Tuple: Features and target arrays
        """
        try:
            # Separate features and target
            X = data.drop(columns=[target_column])
            y = data[target_column]
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Encode target if needed
            if not isinstance(y.iloc[0], (int, float)):
                y = self.label_encoder.fit_transform(y)
            
            return X_scaled, y
        except Exception as e:
            logger.error(f"Error preparing features: {str(e)}")
            raise

    def split_data(
        self,
        X: np.ndarray,
        y: np.ndarray,
        test_size: float = 0.2
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Split data into training and testing sets
        
        Args:
            X (np.ndarray): Feature matrix
            y (np.ndarray): Target vector
            test_size (float): Proportion of data to use for testing
            
        Returns:
            Tuple: Training and testing sets
        """
        try:
            return train_test_split(
                X, y,
                test_size=test_size,
                random_state=self.config['random_state']
            )
        except Exception as e:
            logger.error(f"Error splitting data: {str(e)}")
            raise

    def train_model(
        self,
        model_name: str,
        X_train: np.ndarray,
        y_train: np.ndarray
    ) -> Any:
        """
        Train a model
        
        Args:
            model_name (str): Name of the model to train
            X_train (np.ndarray): Training features
            y_train (np.ndarray): Training target
            
        Returns:
            Any: Trained model
        """
        try:
            if model_name not in self.models:
                raise ValueError(f"Model {model_name} not found")
            
            # Get model
            model = self.models[model_name]
            
            # Train model
            model.fit(X_train, y_train)
            
            logger.info(f"Successfully trained model: {model_name}")
            return model
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise

    def evaluate_model(
        self,
        model: Any,
        X_test: np.ndarray,
        y_test: np.ndarray
    ) -> Dict[str, float]:
        """
        Evaluate a model
        
        Args:
            model (Any): Trained model
            X_test (np.ndarray): Testing features
            y_test (np.ndarray): Testing target
            
        Returns:
            Dict: Evaluation metrics
        """
        try:
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            metrics = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, average='weighted'),
                'recall': recall_score(y_test, y_pred, average='weighted'),
                'f1': f1_score(y_test, y_pred, average='weighted')
            }
            
            return metrics
        except Exception as e:
            logger.error(f"Error evaluating model: {str(e)}")
            raise

    def optimize_hyperparameters(
        self,
        model_name: str,
        X_train: np.ndarray,
        y_train: np.ndarray,
        n_trials: int = 100
    ) -> Dict[str, Any]:
        """
        Optimize model hyperparameters using Optuna
        
        Args:
            model_name (str): Name of the model to optimize
            X_train (np.ndarray): Training features
            y_train (np.ndarray): Training target
            n_trials (int): Number of optimization trials
            
        Returns:
            Dict: Best hyperparameters and metrics
        """
        try:
            def objective(trial):
                # Define hyperparameter search space
                if model_name == 'random_forest':
                    params = {
                        'n_estimators': trial.suggest_int('n_estimators', 10, 100),
                        'max_depth': trial.suggest_int('max_depth', 3, 10),
                        'min_samples_split': trial.suggest_int('min_samples_split', 2, 10),
                        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 5)
                    }
                elif model_name == 'gradient_boosting':
                    params = {
                        'n_estimators': trial.suggest_int('n_estimators', 10, 100),
                        'learning_rate': trial.suggest_loguniform('learning_rate', 0.01, 0.1),
                        'max_depth': trial.suggest_int('max_depth', 3, 10)
                    }
                else:
                    raise ValueError(f"Hyperparameter optimization not implemented for {model_name}")
                
                # Train and evaluate model
                model = self.models[model_name].set_params(**params)
                scores = cross_val_score(model, X_train, y_train, cv=5)
                
                return np.mean(scores)
            
            # Run optimization
            study = optuna.create_study(direction='maximize')
            study.optimize(objective, n_trials=n_trials)
            
            # Get best parameters
            best_params = study.best_params
            best_score = study.best_value
            
            return {
                'best_params': best_params,
                'best_score': best_score
            }
        except Exception as e:
            logger.error(f"Error optimizing hyperparameters: {str(e)}")
            raise

    def save_model(
        self,
        model: Any,
        model_name: str,
        metrics: Dict[str, float]
    ) -> None:
        """
        Save model and metrics
        
        Args:
            model (Any): Trained model
            model_name (str): Name of the model
            metrics (Dict): Model metrics
        """
        try:
            # Create timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save model
            model_path = f"models/{model_name}_{timestamp}.joblib"
            joblib.dump(model, model_path)
            
            # Save metrics
            metrics_path = f"metrics/{model_name}_{timestamp}.json"
            with open(metrics_path, 'w') as f:
                json.dump(metrics, f, indent=2)
            
            logger.info(f"Successfully saved model and metrics")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            raise

    def log_experiment(
        self,
        model_name: str,
        metrics: Dict[str, float],
        params: Dict[str, Any]
    ) -> None:
        """
        Log experiment to MLflow
        
        Args:
            model_name (str): Name of the model
            metrics (Dict): Model metrics
            params (Dict): Model parameters
        """
        try:
            with mlflow.start_run():
                # Log parameters
                mlflow.log_params(params)
                
                # Log metrics
                mlflow.log_metrics(metrics)
                
                # Log model
                mlflow.sklearn.log_model(
                    self.models[model_name],
                    f"model_{model_name}"
                )
            
            logger.info(f"Successfully logged experiment to MLflow")
        except Exception as e:
            logger.error(f"Error logging experiment: {str(e)}")
            raise

    def run_pipeline(
        self,
        data_path: str,
        target_column: str,
        optimize: bool = True
    ) -> Dict[str, Any]:
        """
        Run the complete ML pipeline
        
        Args:
            data_path (str): Path to the data file
            target_column (str): Name of the target column
            optimize (bool): Whether to optimize hyperparameters
            
        Returns:
            Dict: Pipeline results
        """
        try:
            # Load and prepare data
            data = self.load_data(data_path)
            X, y = self.prepare_features(data, target_column)
            
            # Split data
            X_train, X_test, y_train, y_test = self.split_data(X, y)
            
            # Train and evaluate models
            results = {}
            for model_name in self.models.keys():
                print(f"\nTraining {model_name}...")
                
                # Optimize hyperparameters if requested
                if optimize:
                    print("Optimizing hyperparameters...")
                    optimization_results = self.optimize_hyperparameters(
                        model_name,
                        X_train,
                        y_train
                    )
                    self.models[model_name].set_params(**optimization_results['best_params'])
                
                # Train model
                model = self.train_model(model_name, X_train, y_train)
                
                # Evaluate model
                metrics = self.evaluate_model(model, X_test, y_test)
                
                # Save model and metrics
                self.save_model(model, model_name, metrics)
                
                # Log experiment
                self.log_experiment(
                    model_name,
                    metrics,
                    model.get_params()
                )
                
                results[model_name] = {
                    'metrics': metrics,
                    'model': model
                }
            
            self.results = results
            return results
        except Exception as e:
            logger.error(f"Error running pipeline: {str(e)}")
            raise

def main():
    """Example usage of the MLPipeline class"""
    try:
        # Initialize pipeline
        pipeline = MLPipeline()
        
        # Example data path and target column
        data_path = "data.csv"
        target_column = "target"
        
        # Run pipeline
        results = pipeline.run_pipeline(
            data_path,
            target_column,
            optimize=True
        )
        
        # Print results
        print("\nPipeline Results:")
        for model_name, model_results in results.items():
            print(f"\n{model_name.upper()}:")
            print("Metrics:")
            print(json.dumps(model_results['metrics'], indent=2))
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 