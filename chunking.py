from langchain_text_splitters import RecursiveCharacterTextSplitter

# Chunking
def chunk_documents(documents):
  splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
  )

  split_doc = splitter.split_documents(documents)

  print("Chunks:", len(split_doc))
  return split_doc
