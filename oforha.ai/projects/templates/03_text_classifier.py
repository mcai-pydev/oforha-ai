"""
Text Classification Template
A comprehensive text classification system using NLP techniques
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional
import logging

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextClassifier:
    def __init__(self, data_path: str):
        """
        Initialize the TextClassifier with a data file path
        
        Args:
            data_path (str): Path to the text dataset
        """
        self.data_path = data_path
        self.data = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.vectorizer = TfidfVectorizer()
        self.models = {}
        self.nlp = spacy.load('en_core_web_sm')
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.load_data()

    def load_data(self) -> None:
        """Load and prepare the text dataset"""
        try:
            self.data = pd.read_csv(self.data_path)
            logger.info(f"Successfully loaded data from {self.data_path}")
            
            # Prepare features and target
            self.prepare_data()
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def prepare_data(self) -> None:
        """Prepare text features and target variables"""
        # Example columns (modify based on your dataset)
        self.X = self.data['text']
        self.y = self.data['label']

    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text using spaCy and NLTK
        
        Args:
            text (str): Input text
            
        Returns:
            str: Preprocessed text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token not in self.stop_words
        ]
        
        # Join tokens back into text
        return ' '.join(tokens)

    def extract_features(self, text: str) -> Dict[str, float]:
        """
        Extract additional features using spaCy
        
        Args:
            text (str): Input text
            
        Returns:
            Dict: Dictionary of extracted features
        """
        doc = self.nlp(text)
        
        features = {
            'num_tokens': len(doc),
            'num_sentences': len(list(doc.sents)),
            'num_entities': len(doc.ents),
            'num_nouns': len([token for token in doc if token.pos_ == 'NOUN']),
            'num_verbs': len([token for token in doc if token.pos_ == 'VERB']),
            'num_adjectives': len([token for token in doc if token.pos_ == 'ADJ']),
            'num_adverbs': len([token for token in doc if token.pos_ == 'ADV'])
        }
        
        return features

    def split_data(self, test_size: float = 0.2) -> None:
        """
        Split data into training and testing sets
        
        Args:
            test_size (float): Proportion of data to use for testing
        """
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=42
        )
        
        # Preprocess text
        self.X_train_processed = [self.preprocess_text(text) for text in self.X_train]
        self.X_test_processed = [self.preprocess_text(text) for text in self.X_test]
        
        # Vectorize text
        self.X_train_vectorized = self.vectorizer.fit_transform(self.X_train_processed)
        self.X_test_vectorized = self.vectorizer.transform(self.X_test_processed)

    def train_models(self) -> None:
        """Train multiple classification models"""
        # Naive Bayes
        self.models['nb'] = MultinomialNB()
        self.models['nb'].fit(self.X_train_vectorized, self.y_train)
        
        # Logistic Regression
        self.models['lr'] = LogisticRegression(max_iter=1000)
        self.models['lr'].fit(self.X_train_vectorized, self.y_train)
        
        # Random Forest
        self.models['rf'] = RandomForestClassifier(n_estimators=100, random_state=42)
        self.models['rf'].fit(self.X_train_vectorized, self.y_train)

    def evaluate_models(self) -> Dict[str, Dict[str, float]]:
        """
        Evaluate all trained models
        
        Returns:
            Dict: Dictionary containing evaluation metrics for each model
        """
        results = {}
        
        for name, model in self.models.items():
            # Make predictions
            y_pred = model.predict(self.X_test_vectorized)
            
            # Get classification report
            report = classification_report(self.y_test, y_pred, output_dict=True)
            
            results[name] = {
                'accuracy': report['accuracy'],
                'precision': report['weighted avg']['precision'],
                'recall': report['weighted avg']['recall'],
                'f1-score': report['weighted avg']['f1-score']
            }
        
        return results

    def plot_confusion_matrix(self, model_name: str) -> plt.Figure:
        """
        Plot confusion matrix for the specified model
        
        Args:
            model_name (str): Name of the model to use
            
        Returns:
            plt.Figure: Matplotlib figure object
        """
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
            
        model = self.models[model_name]
        y_pred = model.predict(self.X_test_vectorized)
        
        # Create confusion matrix
        cm = confusion_matrix(self.y_test, y_pred)
        
        # Plot confusion matrix
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f'Confusion Matrix - {model_name.upper()}')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.tight_layout()
        
        return plt.gcf()

    def classify_text(self, text: str) -> Dict[str, float]:
        """
        Classify input text using all models
        
        Args:
            text (str): Input text to classify
            
        Returns:
            Dict: Dictionary of predictions and probabilities
        """
        # Preprocess text
        processed_text = self.preprocess_text(text)
        
        # Vectorize text
        vectorized_text = self.vectorizer.transform([processed_text])
        
        # Get predictions from all models
        predictions = {}
        for name, model in self.models.items():
            pred = model.predict(vectorized_text)[0]
            prob = model.predict_proba(vectorized_text)[0]
            predictions[name] = {
                'prediction': pred,
                'probability': float(max(prob))
            }
        
        return predictions

def main():
    """Example usage of the TextClassifier class"""
    # Example data path
    data_path = "text_data.csv"
    
    try:
        # Initialize classifier
        classifier = TextClassifier(data_path)
        
        # Split data
        classifier.split_data()
        
        # Train models
        classifier.train_models()
        
        # Evaluate models
        results = classifier.evaluate_models()
        print("Model Evaluation Results:", results)
        
        # Plot confusion matrix
        fig = classifier.plot_confusion_matrix('rf')
        fig.savefig('confusion_matrix.png')
        
        # Example classification
        sample_text = "This is an example text for classification."
        predictions = classifier.classify_text(sample_text)
        print("Classification Results:", predictions)
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 