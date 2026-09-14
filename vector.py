import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


DB_DIR = "rag-db"


def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if os.path.exists(DB_DIR) and os.listdir(DB_DIR):
        # Store already exists
        print("Existing vector store found.")

        vector_store = Chroma(
            persist_directory=DB_DIR,
            embedding_function=embeddings
        )

        # Get metadata of existing chunks
        data = vector_store.get(include=["metadatas"])

        # Get unique source filenames already in the database
        existing_sources = {
            metadata.get("source")
            for metadata in data["metadatas"]
        }

        # Get the source filename of the new document
        new_source = chunks[0].metadata.get("source")

        # Check if the document is already present
        if new_source in existing_sources:
            print(f"'{new_source}' already exists. Skipping.")
            return vector_store, False

        # New document -> add its chunks
        print(f"Adding new document: {new_source}")
        vector_store.add_documents(chunks)

        return vector_store, True

    else:
        # First document -> create a fresh store
        print("No existing store found. Creating new vector store...")

        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=DB_DIR
        )

        return vector_store, True


def delete_vector_store(vector_store):
    """
    Delete the Chroma knowledge-base collection.
    """

    if vector_store is None:
        print("No vector store to delete.")
        return

    vector_store.delete_collection()

    print("Knowledge base collection deleted successfully.")
