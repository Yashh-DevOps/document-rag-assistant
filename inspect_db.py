from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = Chroma(persist_directory="rag-db", embedding_function=embeddings)

# Fetch everything currently stored (metadata + documents, no vectors needed)
data = vector_store.get(include=["metadatas", "documents"])

total_chunks = len(data["ids"])
sources = sorted({meta.get("source", "Unknown") for meta in data["metadatas"]})

print(f"Total chunks in DB: {total_chunks}")
print(f"Unique source files: {len(sources)}")
print("-" * 40)
for src in sources:
    count = sum(1 for meta in data["metadatas"] if meta.get("source") == src)
    print(f"  {src}  ->  {count} chunks")