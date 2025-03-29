"""
Multi-language Text Analyzer Template
A comprehensive text analysis system supporting multiple languages
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from sentence_transformers import SentenceTransformer
import spacy
from langdetect import detect, detect_langs
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from pathlib import Path
import json
import os

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiLanguageAnalyzer:
    def __init__(
        self,
        supported_languages: List[str] = ['en', 'es', 'fr', 'de', 'it'],
        sentiment_model: str = "nlptown/bert-base-multilingual-uncased-sentiment",
        topic_model: str = "facebook/bart-large-mnli"
    ):
        """
        Initialize the MultiLanguageAnalyzer
        
        Args:
            supported_languages (List[str]): List of supported language codes
            sentiment_model (str): Name of the sentiment analysis model
            topic_model (str): Name of the topic classification model
        """
        self.supported_languages = supported_languages
        self.sentiment_model = sentiment_model
        self.topic_model = topic_model
        
        # Initialize models and tools
        self.initialize_models()
        self.initialize_nlp_tools()
        
        # Store results
        self.analysis_results = {}

    def initialize_models(self) -> None:
        """Initialize transformer models"""
        try:
            # Initialize sentiment analysis
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model=self.sentiment_model
            )
            
            # Initialize topic classification
            self.topic_classifier = pipeline(
                "zero-shot-classification",
                model=self.topic_model
            )
            
            # Initialize sentence transformer for embeddings
            self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            
            logger.info("Successfully initialized transformer models")
        except Exception as e:
            logger.error(f"Error initializing models: {str(e)}")
            raise

    def initialize_nlp_tools(self) -> None:
        """Initialize NLP tools for each supported language"""
        try:
            self.nlp_tools = {}
            for lang in self.supported_languages:
                try:
                    self.nlp_tools[lang] = spacy.load(f"{lang}_core_news_sm")
                except:
                    logger.warning(f"Could not load spaCy model for language: {lang}")
            
            # Initialize NLTK tools
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = {
                lang: set(stopwords.words(lang))
                for lang in self.supported_languages
            }
            
            logger.info("Successfully initialized NLP tools")
        except Exception as e:
            logger.error(f"Error initializing NLP tools: {str(e)}")
            raise

    def detect_language(self, text: str) -> str:
        """
        Detect the language of the input text
        
        Args:
            text (str): Input text
            
        Returns:
            str: Detected language code
        """
        try:
            return detect(text)
        except Exception as e:
            logger.error(f"Error detecting language: {str(e)}")
            raise

    def get_language_probabilities(self, text: str) -> List[Dict[str, float]]:
        """
        Get probabilities for different languages
        
        Args:
            text (str): Input text
            
        Returns:
            List[Dict]: List of language probabilities
        """
        try:
            return detect_langs(text)
        except Exception as e:
            logger.error(f"Error getting language probabilities: {str(e)}")
            raise

    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of the text
        
        Args:
            text (str): Input text
            
        Returns:
            Dict: Sentiment analysis results
        """
        try:
            result = self.sentiment_analyzer(text)[0]
            return {
                'label': result['label'],
                'score': float(result['score'])
            }
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            raise

    def classify_topic(
        self,
        text: str,
        candidate_topics: List[str] = None
    ) -> Dict:
        """
        Classify the topic of the text
        
        Args:
            text (str): Input text
            candidate_topics (List[str]): List of possible topics
            
        Returns:
            Dict: Topic classification results
        """
        try:
            if candidate_topics is None:
                candidate_topics = [
                    "technology", "business", "sports", "entertainment",
                    "politics", "science", "health", "education"
                ]
            
            result = self.topic_classifier(
                text,
                candidate_topics,
                multi_label=True
            )
            
            return {
                'topics': result['labels'],
                'scores': [float(score) for score in result['scores']]
            }
        except Exception as e:
            logger.error(f"Error classifying topic: {str(e)}")
            raise

    def extract_entities(self, text: str, lang: str) -> List[Dict]:
        """
        Extract named entities from the text
        
        Args:
            text (str): Input text
            lang (str): Language code
            
        Returns:
            List[Dict]: List of extracted entities
        """
        try:
            if lang not in self.nlp_tools:
                raise ValueError(f"Language {lang} not supported")
            
            doc = self.nlp_tools[lang](text)
            entities = []
            
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char
                })
            
            return entities
        except Exception as e:
            logger.error(f"Error extracting entities: {str(e)}")
            raise

    def analyze_text_structure(self, text: str, lang: str) -> Dict:
        """
        Analyze text structure (tokens, sentences, etc.)
        
        Args:
            text (str): Input text
            lang (str): Language code
            
        Returns:
            Dict: Text structure analysis results
        """
        try:
            # Tokenize
            tokens = word_tokenize(text, language=lang)
            sentences = sent_tokenize(text, language=lang)
            
            # Get part-of-speech tags
            pos_tags = nltk.pos_tag(tokens)
            
            # Lemmatize tokens
            lemmatized_tokens = [
                self.lemmatizer.lemmatize(token)
                for token in tokens
                if token not in self.stop_words.get(lang, set())
            ]
            
            return {
                'num_tokens': len(tokens),
                'num_sentences': len(sentences),
                'num_unique_tokens': len(set(tokens)),
                'num_lemmatized_tokens': len(lemmatized_tokens),
                'pos_tags': pos_tags
            }
        except Exception as e:
            logger.error(f"Error analyzing text structure: {str(e)}")
            raise

    def get_text_embeddings(self, text: str) -> np.ndarray:
        """
        Get text embeddings
        
        Args:
            text (str): Input text
            
        Returns:
            np.ndarray: Text embeddings
        """
        try:
            return self.embedding_model.encode(text)
        except Exception as e:
            logger.error(f"Error getting text embeddings: {str(e)}")
            raise

    def analyze_text(
        self,
        text: str,
        save_results: bool = False,
        output_path: Optional[str] = None
    ) -> Dict:
        """
        Perform comprehensive text analysis
        
        Args:
            text (str): Input text
            save_results (bool): Whether to save results to file
            output_path (Optional[str]): Path to save results
            
        Returns:
            Dict: Comprehensive analysis results
        """
        try:
            # Detect language
            lang = self.detect_language(text)
            lang_probs = self.get_language_probabilities(text)
            
            # Perform analysis
            results = {
                'language': {
                    'detected': lang,
                    'probabilities': lang_probs
                },
                'sentiment': self.analyze_sentiment(text),
                'topic': self.classify_topic(text),
                'entities': self.extract_entities(text, lang),
                'structure': self.analyze_text_structure(text, lang),
                'embeddings': self.get_text_embeddings(text).tolist()
            }
            
            # Store results
            self.analysis_results[text] = results
            
            # Save results if requested
            if save_results and output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
            
            return results
        except Exception as e:
            logger.error(f"Error analyzing text: {str(e)}")
            raise

    def plot_analysis_results(
        self,
        text: str,
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Plot analysis results
        
        Args:
            text (str): Input text
            save_path (Optional[str]): Path to save the plot
            
        Returns:
            plt.Figure: Matplotlib figure object
        """
        try:
            if text not in self.analysis_results:
                raise ValueError("Text not analyzed yet")
            
            results = self.analysis_results[text]
            
            # Create subplots
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            
            # Plot sentiment
            sentiment = results['sentiment']
            axes[0, 0].bar(['Negative', 'Positive'], [1 - sentiment['score'], sentiment['score']])
            axes[0, 0].set_title('Sentiment Analysis')
            
            # Plot topic scores
            topics = results['topic']
            axes[0, 1].bar(topics['topics'], topics['scores'])
            axes[0, 1].set_title('Topic Classification')
            axes[0, 1].tick_params(axis='x', rotation=45)
            
            # Plot language probabilities
            lang_probs = results['language']['probabilities']
            axes[1, 0].bar(
                [p.lang for p in lang_probs],
                [p.prob for p in lang_probs]
            )
            axes[1, 0].set_title('Language Probabilities')
            
            # Plot text structure
            structure = results['structure']
            axes[1, 1].bar(
                ['Tokens', 'Sentences', 'Unique Tokens'],
                [structure['num_tokens'], structure['num_sentences'], structure['num_unique_tokens']]
            )
            axes[1, 1].set_title('Text Structure')
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path)
            
            return fig
        except Exception as e:
            logger.error(f"Error plotting results: {str(e)}")
            raise

def main():
    """Example usage of the MultiLanguageAnalyzer class"""
    try:
        # Initialize analyzer
        analyzer = MultiLanguageAnalyzer()
        
        # Example texts in different languages
        texts = [
            "I love this product! It's amazing and works perfectly.",
            "¡Este producto es excelente! Me encanta cómo funciona.",
            "Ce produit est fantastique ! Je l'adore.",
            "Dieses Produkt ist großartig! Ich liebe es.",
            "Questo prodotto è fantastico! Lo adoro."
        ]
        
        # Analyze each text
        for i, text in enumerate(texts):
            print(f"\nAnalyzing text {i+1}:")
            print(f"Text: {text}")
            
            # Perform analysis
            results = analyzer.analyze_text(
                text,
                save_results=True,
                output_path=f'analysis_results_{i+1}.json'
            )
            
            # Print key results
            print(f"Detected Language: {results['language']['detected']}")
            print(f"Sentiment: {results['sentiment']['label']}")
            print(f"Main Topics: {results['topic']['topics'][:3]}")
            
            # Plot results
            fig = analyzer.plot_analysis_results(
                text,
                save_path=f'analysis_plot_{i+1}.png'
            )
            plt.close(fig)
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 