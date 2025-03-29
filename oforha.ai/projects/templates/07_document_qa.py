"""
Document Q&A System Template
A comprehensive question-answering system for documents using RAG and transformers
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
from sentence_transformers import SentenceTransformer
import faiss
import chromadb
from chromadb.config import Settings
import spacy
from nltk.tokenize import sent_tokenize
import logging
from pathlib import Path
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentQASystem:
    def __init__(
        self,
        qa_model: str = "deepset/roberta-base-squad2",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        index_path: str = "faiss_index",
        collection_name: str = "documents"
    ):
        """
        Initialize the DocumentQASystem
        
        Args:
            qa_model (str): Name of the question-answering model
            embedding_model (str): Name of the sentence transformer model
            index_path (str): Path to save/load the FAISS index
            collection_name (str): Name of the ChromaDB collection
        """
        self.qa_model = qa_model
        self.embedding_model = embedding_model
        self.index_path = index_path
        self.collection_name = collection_name
        
        # Initialize models and databases
        self.initialize_models()
        self.initialize_databases()
        
        # Load or create index
        self.load_or_create_index()
        
        # Store results
        self.qa_history = []

    def initialize_models(self) -> None:
        """Initialize transformer models"""
        try:
            # Initialize QA model
            self.qa_pipeline = pipeline(
                "question-answering",
                model=self.qa_model
            )
            
            # Initialize embedding model
            self.embedding_model = SentenceTransformer(self.embedding_model)
            
            # Initialize spaCy for text processing
            self.nlp = spacy.load("en_core_web_sm")
            
            logger.info("Successfully initialized transformer models")
        except Exception as e:
            logger.error(f"Error initializing models: {str(e)}")
            raise

    def initialize_databases(self) -> None:
        """Initialize ChromaDB client"""
        try:
            self.client = chromadb.Client(Settings(
                persist_directory="./chroma_db",
                anonymized_telemetry=False
            ))
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name
            )
            logger.info(f"Successfully initialized ChromaDB collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {str(e)}")
            raise

    def load_or_create_index(self) -> None:
        """Load existing FAISS index or create a new one"""
        try:
            if os.path.exists(self.index_path):
                self.index = faiss.read_index(self.index_path)
                logger.info(f"Successfully loaded FAISS index from {self.index_path}")
            else:
                # Create a new index with the correct dimension
                dimension = self.embedding_model.get_sentence_embedding_dimension()
                self.index = faiss.IndexFlatL2(dimension)
                logger.info(f"Created new FAISS index with dimension {dimension}")
        except Exception as e:
            logger.error(f"Error loading/creating FAISS index: {str(e)}")
            raise

    def process_document(self, text: str, doc_id: str) -> None:
        """
        Process and index a document
        
        Args:
            text (str): Document text
            doc_id (str): Unique document identifier
        """
        try:
            # Split text into sentences
            sentences = sent_tokenize(text)
            
            # Generate embeddings
            embeddings = self.embedding_model.encode(sentences)
            
            # Add to FAISS index
            self.index.add(np.array(embeddings).astype('float32'))
            
            # Add to ChromaDB
            self.collection.add(
                documents=sentences,
                embeddings=embeddings.tolist(),
                metadatas=[{"doc_id": doc_id, "sentence_index": i} for i in range(len(sentences))],
                ids=[f"{doc_id}_sent_{i}" for i in range(len(sentences))]
            )
            
            # Save the updated index
            faiss.write_index(self.index, self.index_path)
            
            logger.info(f"Successfully processed document: {doc_id}")
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise

    def retrieve_relevant_context(
        self,
        query: str,
        k: int = 5
    ) -> List[str]:
        """
        Retrieve relevant context for a query
        
        Args:
            query (str): User query
            k (int): Number of relevant sentences to retrieve
            
        Returns:
            List[str]: List of relevant sentences
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])[0]
            
            # Search in FAISS
            distances, indices = self.index.search(
                np.array([query_embedding]).astype('float32'),
                k
            )
            
            # Get results from ChromaDB
            results = self.collection.get(
                ids=[f"doc_{idx}" for idx in indices[0]]
            )
            
            return results['documents']
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            raise

    def answer_question(
        self,
        question: str,
        context: Optional[List[str]] = None,
        doc_id: Optional[str] = None
    ) -> Dict:
        """
        Answer a question using the QA model
        
        Args:
            question (str): User question
            context (Optional[List[str]]): List of relevant context sentences
            doc_id (Optional[str]): Document identifier
            
        Returns:
            Dict: Answer and metadata
        """
        try:
            # If no context provided, retrieve relevant context
            if context is None:
                context = self.retrieve_relevant_context(question)
            
            # Combine context into a single string
            context_text = " ".join(context)
            
            # Get answer from QA model
            result = self.qa_pipeline(
                question=question,
                context=context_text
            )
            
            # Create response
            response = {
                'answer': result['answer'],
                'confidence': float(result['score']),
                'context': context,
                'doc_id': doc_id,
                'question': question
            }
            
            # Store in history
            self.qa_history.append(response)
            
            return response
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            raise

    def update_document(
        self,
        doc_id: str,
        new_text: str
    ) -> None:
        """
        Update an existing document
        
        Args:
            doc_id (str): ID of the document to update
            new_text (str): New document text
        """
        try:
            # Delete old document
            self.delete_document(doc_id)
            
            # Process new document
            self.process_document(new_text, doc_id)
            
            logger.info(f"Successfully updated document: {doc_id}")
        except Exception as e:
            logger.error(f"Error updating document: {str(e)}")
            raise

    def delete_document(self, doc_id: str) -> None:
        """
        Delete a document from the system
        
        Args:
            doc_id (str): ID of the document to delete
        """
        try:
            # Delete from ChromaDB
            self.collection.delete(
                where={"doc_id": doc_id}
            )
            logger.info(f"Successfully deleted document: {doc_id}")
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            raise

    def get_qa_history(
        self,
        doc_id: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Get question-answering history
        
        Args:
            doc_id (Optional[str]): Filter by document ID
            limit (Optional[int]): Limit number of results
            
        Returns:
            List[Dict]: List of QA history entries
        """
        try:
            history = self.qa_history
            
            # Filter by document ID if specified
            if doc_id:
                history = [entry for entry in history if entry['doc_id'] == doc_id]
            
            # Apply limit if specified
            if limit:
                history = history[-limit:]
            
            return history
        except Exception as e:
            logger.error(f"Error getting QA history: {str(e)}")
            raise

    def evaluate_qa_performance(
        self,
        test_questions: List[Dict[str, str]]
    ) -> Dict:
        """
        Evaluate QA system performance
        
        Args:
            test_questions (List[Dict]): List of test questions with ground truth
            
        Returns:
            Dict: Performance metrics
        """
        try:
            results = []
            for test in test_questions:
                # Get answer
                answer = self.answer_question(
                    test['question'],
                    context=test.get('context')
                )
                
                # Compare with ground truth
                results.append({
                    'question': test['question'],
                    'predicted': answer['answer'],
                    'ground_truth': test['answer'],
                    'confidence': answer['confidence']
                })
            
            # Calculate metrics
            metrics = {
                'total_questions': len(results),
                'average_confidence': np.mean([r['confidence'] for r in results]),
                'exact_matches': sum(
                    1 for r in results
                    if r['predicted'].lower() == r['ground_truth'].lower()
                )
            }
            
            return metrics
        except Exception as e:
            logger.error(f"Error evaluating performance: {str(e)}")
            raise

def main():
    """Example usage of the DocumentQASystem class"""
    try:
        # Initialize QA system
        qa_system = DocumentQASystem()
        
        # Example document
        document = """
        Machine learning is a field of study that gives computers the ability to learn without being explicitly programmed.
        Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence
        concerned with the interactions between computers and human language. Deep learning is part of a broader family
        of machine learning methods based on artificial neural networks with representation learning.
        """
        
        # Process document
        qa_system.process_document(document, "doc_1")
        
        # Example questions
        questions = [
            "What is machine learning?",
            "What is NLP?",
            "What is deep learning?"
        ]
        
        # Answer questions
        for question in questions:
            print(f"\nQuestion: {question}")
            answer = qa_system.answer_question(question)
            print(f"Answer: {answer['answer']}")
            print(f"Confidence: {answer['confidence']:.2f}")
        
        # Get QA history
        history = qa_system.get_qa_history()
        print("\nQA History:")
        for entry in history:
            print(f"Q: {entry['question']}")
            print(f"A: {entry['answer']}")
        
        # Example performance evaluation
        test_questions = [
            {
                "question": "What is machine learning?",
                "answer": "Machine learning is a field of study that gives computers the ability to learn without being explicitly programmed.",
                "context": None
            }
        ]
        
        metrics = qa_system.evaluate_qa_performance(test_questions)
        print("\nPerformance Metrics:")
        print(json.dumps(metrics, indent=2))
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 