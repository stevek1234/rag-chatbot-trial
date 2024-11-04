import fitz
import hashlib
import os

def init_openai():
    import openai
    openai.api_key = os.getenv('OPENAI_API_KEY')


def init_pinecone(index_name):
    from pinecone import Pinecone
    # Initialize Pinecone with environment and index name
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    return pc.Index(index_name)


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    with fitz.open(pdf_path) as pdf:
        text_content = [page.get_text() for page in pdf]
    return text_content


def get_embedding(text):
    """Generate an embedding for the given text using OpenAI."""
    import openai
    response = openai.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding


def generate_document_id(text):
    """Generate a unique ID for the document based on its content."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()



