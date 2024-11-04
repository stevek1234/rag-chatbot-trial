import os
import shutil

# Updated paths after moving FilesToUpload outside of backend
base_folder = os.path.join("..", "FilesToUpload")
upload_folder = os.path.join(base_folder, "UploadedFiles")

# # Ensure the upload folder exists
os.makedirs(upload_folder, exist_ok=True)


batch_size = 100


def upload_pdf_to_pinecone(pdf_path):
    """Uploads a PDF to Pinecone in batches after extracting text."""
    from document_processing import extract_text_from_pdf, get_embedding
    from document_processing import generate_document_id, init_openai, init_pinecone

    # Initialize OpenAI and Pinecone
    init_openai()
    index = init_pinecone("initial-rag")

    # Extract text from PDF in chunks
    document_chunks = extract_text_from_pdf(pdf_path)

    # Process in batches
    for i in range(0, len(document_chunks), batch_size):
        chunk_batch = document_chunks[i:i + batch_size]

        # Generate embeddings and metadata for each chunk
        embeddings = [get_embedding(chunk) for chunk in chunk_batch]
        metadata = [{"text": chunk} for chunk in chunk_batch]
        ids = [generate_document_id(chunk) for chunk in chunk_batch]

        # Prepare data to upsert
        to_upsert = list(zip(ids, embeddings, metadata))

        # Upsert batch to Pinecone
        index.upsert(vectors=to_upsert)
        print(f"Uploaded batch {i // batch_size + 1} of {len(document_chunks) // batch_size + 1}")


def process_all_pdfs():
    """Processes all PDF files in FilesToUpload, uploads them, and moves to UploadedFiles."""
    for filename in os.listdir(base_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(base_folder, filename)
            print(f"Processing file: {filename}")

            # Upload PDF to Pinecone
            upload_pdf_to_pinecone(pdf_path)

            # Move PDF to UploadedFiles folder
            shutil.move(pdf_path, os.path.join(upload_folder, filename))
            print(f"Moved {filename} to UploadedFiles")


# # Example usage
# if __name__ == "__main__":
#     process_all_pdfs()

