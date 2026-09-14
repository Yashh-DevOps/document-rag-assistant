from langchain_community.document_loaders import PyPDFLoader , TextLoader , Docx2txtLoader

def load_document(file_path):
    if file_path.endswith(".pdf") or file_path.endswith(".PDF"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".txt") or  file_path.endswith(".TXT"):
        loader = TextLoader(file_path)
    elif file_path.endswith(".docx") or file_path.endswith(".DOCX"):
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError("Unsupported file type")

    documents = loader.load()
    print("Pages:", len(documents))
    return documents


