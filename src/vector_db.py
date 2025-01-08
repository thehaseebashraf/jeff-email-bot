# vector_db.py
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from qdrant_client import QdrantClient
import re

# Configuration constants
QDRANT_URL = "https://0226cf72-a7d5-4bf6-be5f-7f78f89f6733.europe-west3-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "_2Pmz-cQGsZCcgw5EW8YAjH31vh5XHlvSSCp7mF6scPMOJSsLXNm3g"

def clean_text(text):
    """Clean text by removing extra whitespace and newlines"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def search_similar_content(search_text, top_k=3):
    """
    Search for similar content using direct text input
    
    Args:
        search_text: Text to search for
        top_k: Number of similar documents to return
    
    Returns:
        List of similar documents with their scores
    """
    try:
        search_text = clean_text(search_text)

        # Initialize embedding model
        embeddings = HuggingFaceBgeEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Create query embedding
        query_vector = embeddings.embed_query(search_text)
        
        # Initialize Qdrant client
        client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY
        )
        
        # Search with payload included
        results = client.search(
            collection_name="qa_index",
            query_vector=query_vector,
            limit=top_k,
            with_payload=True
        )
        
        # Format and print results
        formatted_results = []
        print(f"\nSearch Results for: {search_text}")
        print("-" * 80)
        
        for result in results:
            formatted_result = {
                'score': result.score,
                'content': result.payload.get('text', 'No content'),
                'source': result.payload.get('source', 'Unknown'),
                'title': result.payload.get('title', 'Unknown')
            }
            
            # Print each result
            print(f"\nScore: {formatted_result['score']:.4f}")
            print(f"Title: {formatted_result['title']}")
            print(f"Content: {formatted_result['content']}")
            print("-" * 80)
            
            formatted_results.append(formatted_result)
        
        return formatted_results
        
    except Exception as e:
        print(f"Error searching vector database: {str(e)}")
        raise

def test_search():
    """Test function with some sample searches"""
    query = "what is solutioninn refund policy"
    
    try:
        search_similar_content(query)
    except Exception as e:
        print(f"Error testing query '{query}': {e}")

if __name__ == "__main__":
    test_search()