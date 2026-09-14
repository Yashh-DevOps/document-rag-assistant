# Document RAG Assistant

A document-based **Retrieval-Augmented Generation (RAG)** application that enables users to upload documents and ask context-aware questions about their content.

The application combines document loading, text chunking, embedding generation, vector storage, semantic retrieval, and large language model inference to provide relevant answers based on uploaded documents.

## Features

* Upload and process multiple document formats:

  * PDF
  * TXT
  * Markdown
  * DOCX
* Extract text from uploaded documents.
* Split documents into smaller chunks for efficient processing and retrieval.
* Generate semantic vector embeddings using Hugging Face.
* Store document embeddings in ChromaDB.
* Retrieve relevant document content using similarity search.
* Generate context-aware answers using Groq LLMs.
* Maintain conversation history for follow-up questions.
* Interact with documents through a Streamlit-based web interface.

## Tech Stack

| Technology    | Purpose                                   |
| ------------- | ----------------------------------------- |
| Python        | Application development                   |
| Streamlit     | Interactive web interface                 |
| LangChain     | RAG workflow and LLM integration          |
| Groq          | Large language model inference            |
| Hugging Face  | Text embedding generation                 |
| ChromaDB      | Vector database and similarity search     |
| PyPDF         | PDF document loading and text extraction  |
| Docx2txt      | DOCX document loading and text extraction |
| python-dotenv | Environment variable management           |

## Application Workflow

```text
Upload Document
       |
       v
Load and Extract Text
       |
       v
Split Text into Chunks
       |
       v
Generate Vector Embeddings
       |
       v
Store Embeddings in ChromaDB
       |
       v
Retrieve Relevant Document Context
       |
       v
Send Context and Question to Groq LLM
       |
       v
Generate Context-Aware Answer
       |
       v
Display Answer in Streamlit
```

## Supported File Formats

| File Format | Supported |
| ----------- | --------- |
| PDF         | Yes       |
| TXT         | Yes       |
| Markdown    | Yes       |
| DOCX        | Yes       |

## Project Structure

```text
document-rag-assistant/
│
├── app.py                  # Streamlit application
├── loader.py               # Document loading and text extraction
├── chunking.py             # Text splitting and chunk creation
├── vector.py               # Embedding generation and vector storage
├── retrieval.py            # Document retrieval logic
├── rag.py                  # RAG question-answering workflow
├── prompt.py               # LLM prompt template
├── inspect_db.py           # Utility for inspecting the vector database
│
├── requirements.txt        # Main project dependencies
├── requirements-full.txt   # Complete frozen environment dependencies
├── .env                    # Environment variables
├── .gitignore              # Git ignored files
└── README.md               # Project documentation
```

## Requirements Files

This project contains two dependency files.

### `requirements.txt`

This file contains the primary dependencies required to install and run the application.

It is the recommended file for normal project setup.

Install the dependencies using:

```bash
pip install -r requirements.txt
```

### `requirements-full.txt`

This file contains the complete list of installed Python packages and their exact versions.

It was generated using:

```bash
pip freeze > requirements-full.txt
```

This file can be used when you need to reproduce the complete development environment.

Install the complete frozen environment using:

```bash
pip install -r requirements-full.txt
```

> **Recommendation:** Use `requirements.txt` for normal installation. Use `requirements-full.txt` when reproducing the complete development environment with the same package versions.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yash-devops/document-rag-assistant.git
cd document-rag-assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

#### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

#### Linux/macOS

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

For the standard installation:

```bash
pip install -r requirements.txt
```

For the complete frozen environment:

```bash
pip install -r requirements-full.txt
```

## Environment Configuration

Create a `.env` file in the root directory of the project.

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

Replace `your_groq_api_key` with your actual Groq API key.

> **Security:** Never commit your `.env` file, API keys, or other sensitive credentials to GitHub.

## Run the Application

Start the Streamlit application using:

```bash
streamlit run app.py
```

The application will open in your default browser.

## How to Use

1. Start the Streamlit application.
2. Upload a supported document.
3. Wait for the document to be processed.
4. Enter a question related to the uploaded document.
5. Submit the question.
6. Review the generated response.
7. Ask follow-up questions using the conversation history.

## Example Use Cases

The application can be used for:

* Asking questions about study materials.
* Searching information inside technical documentation.
* Understanding project reports.
* Exploring research papers.
* Querying business documents.
* Learning from books, notes, and manuals.
* Finding relevant information across uploaded documents.
* Having context-aware conversations with document content.

## Important Notes

The application generates answers based on the information retrieved from uploaded documents.

The quality of the response depends on:

* The content and quality of the uploaded document.
* The text extraction process.
* The chunking strategy.
* The retrieval quality.
* The selected language model.

If the required information is not available in the uploaded document, the application may respond that the information could not be found.

## Security Notes

* Store API keys in environment variables.
* Do not hardcode API keys in Python files.
* Do not commit `.env` files to GitHub.
* Add sensitive files to `.gitignore`.
* Do not upload real API keys in example files.
* If an API key is exposed, revoke it and generate a new one.

## Future Improvements

Potential future improvements include:

* Support for additional document formats.
* Multiple document collections.
* Source citations in generated answers.
* Improved document management.
* Persistent chat history.
* User authentication.
* Cloud deployment.
* Streaming LLM responses.
* Advanced retrieval techniques.
* Document summarization.
* Document comparison.
* Hybrid search and reranking.
* Improved error handling and monitoring.

## License

This project is intended for educational and personal development purposes.

## Author

**Yash Soni**

GitHub: [@Yashh-DevOps](https://github.com/Yashh-DevOps)
