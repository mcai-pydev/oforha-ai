"""
RAG System Template
A comprehensive Retrieval-Augmented Generation system using FAISS and transformers
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
import faiss
from transformers import AutoTokenizer, AutoModel
import torch
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import logging
from pathlib import Path
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGSystem:
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        index_path: str = "faiss_index",
        collection_name: str = "documents"
    ):
        """
        Initialize the RAG system
        
        Args:
            model_name (str): Name of the sentence transformer model to use
            index_path (str): Path to save/load the FAISS index
            collection_name (str): Name of the ChromaDB collection
        """
        self.model_name = model_name
        self.index_path = index_path
        self.collection_name = collection_name
        
        # Initialize models and databases
        self.initialize_models()
        self.initialize_databases()
        
        # Load or create index
        self.load_or_create_index()

    def initialize_models(self) -> None:
        """Initialize the sentence transformer model"""
        try:
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Successfully loaded model: {self.model_name}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
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
                dimension = self.model.get_sentence_embedding_dimension()
                self.index = faiss.IndexFlatL2(dimension)
                logger.info(f"Created new FAISS index with dimension {dimension}")
        except Exception as e:
            logger.error(f"Error loading/creating FAISS index: {str(e)}")
            raise

    def add_documents(
        self,
        documents: List[str],
        metadata: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None
    ) -> None:
        """
        Add documents to the RAG system
        
        Args:
            documents (List[str]): List of document texts
            metadata (Optional[List[Dict]]): List of metadata dictionaries
            ids (Optional[List[str]]): List of document IDs
        """
        try:
            # Generate embeddings
            embeddings = self.model.encode(documents)
            
            # Add to FAISS index
            self.index.add(np.array(embeddings).astype('float32'))
            
            # Add to ChromaDB
            if metadata is None:
                metadata = [{} for _ in documents]
            if ids is None:
                ids = [f"doc_{i}" for i in range(len(documents))]
            
            self.collection.add(
                documents=documents,
                embeddings=embeddings.tolist(),
                metadatas=metadata,
                ids=ids
            )
            
            # Save the updated index
            faiss.write_index(self.index, self.index_path)
            
            logger.info(f"Successfully added {len(documents)} documents to the system")
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise

    def search(
        self,
        query: str,
        k: int = 5,
        return_metadata: bool = True
    ) -> List[Dict]:
        """
        Search for relevant documents
        
        Args:
            query (str): Search query
            k (int): Number of results to return
            return_metadata (bool): Whether to return metadata
            
        Returns:
            List[Dict]: List of relevant documents with their metadata
        """
        try:
            # Generate query embedding
            query_embedding = self.model.encode([query])[0]
            
            # Search in FAISS
            distances, indices = self.index.search(
                np.array([query_embedding]).astype('float32'),
                k
            )
            
            # Get results from ChromaDB
            results = self.collection.get(
                ids=[f"doc_{idx}" for idx in indices[0]]
            )
            
            # Format results
            formatted_results = []
            for i, (doc, distance) in enumerate(zip(results['documents'], distances[0])):
                result = {
                    'document': doc,
                    'distance': float(distance)
                }
                if return_metadata:
                    result['metadata'] = results['metadatas'][i]
                formatted_results.append(result)
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            raise

    def update_document(
        self,
        doc_id: str,
        new_text: str,
        new_metadata: Optional[Dict] = None
    ) -> None:
        """
        Update an existing document
        
        Args:
            doc_id (str): ID of the document to update
            new_text (str): New document text
            new_metadata (Optional[Dict]): New metadata
        """
        try:
            # Generate new embedding
            new_embedding = self.model.encode([new_text])[0]
            
            # Update in ChromaDB
            self.collection.update(
                ids=[doc_id],
                documents=[new_text],
                embeddings=[new_embedding.tolist()],
                metadatas=[new_metadata] if new_metadata else None
            )
            
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
            self.collection.delete(ids=[doc_id])
            logger.info(f"Successfully deleted document: {doc_id}")
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            raise

    def get_document_count(self) -> int:
        """
        Get the total number of documents in the system
        
        Returns:
            int: Number of documents
        """
        return self.collection.count()

def main():
    """Example usage of the RAGSystem class"""
    try:
        # Initialize RAG system
        rag = RAGSystem()
        
        # Example documents
        documents = [
            "Machine learning is a field of study that gives computers the ability to learn without being explicitly programmed.",
            "Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language.",
            "Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning."
        ]
        
        # Example metadata
        metadata = [
            {"topic": "machine_learning", "source": "wikipedia"},
            {"topic": "nlp", "source": "wikipedia"},
            {"topic": "deep_learning", "source": "wikipedia"}
        ]
        
        # Add documents
        rag.add_documents(documents, metadata)
        
        # Search example
        query = "What is machine learning?"
        results = rag.search(query, k=2)
        print("Search Results:", results)
        
        # Update document example
        rag.update_document(
            "doc_0",
            "Machine learning is a field of study that enables computers to learn from data without explicit programming.",
            {"topic": "machine_learning", "source": "updated"}
        )
        
        # Get document count
        count = rag.get_document_count()
        print(f"Total documents: {count}")
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 