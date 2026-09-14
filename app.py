import os
import tempfile

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from loader import load_document
from chunking import chunk_documents
from vector import create_vector_store, delete_vector_store
from retrieval import create_retriever
from prompt import create_prompt
from rag import ask_question


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key and "GROQ_API_KEY" in st.secrets:
    groq_api_key = st.secrets["GROQ_API_KEY"]

st.set_page_config(
    page_title="Doc Q&A",
    page_icon="📄"
)

st.title("DevOps assistant: Ask questions about your documents")


# ---- Session state setup ----

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

if "confirm_clear" not in st.session_state:
    st.session_state.confirm_clear = False


# ---- Load existing vector database ----

if (
    st.session_state.retriever is None
    and os.path.exists("rag-db")
    and os.listdir("rag-db")
):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    st.session_state.vector_store = Chroma(
        persist_directory="rag-db",
        embedding_function=embeddings
    )

    st.session_state.retriever = create_retriever(
        st.session_state.vector_store
    )


# ---- LLM ----
if not groq_api_key:
    st.error("GROQ_API_KEY is missing. Add it to your .env file or Streamlit Secrets.")
    st.stop()

llm = ChatGroq(
    api_key=groq_api_key,
    model="openai/gpt-oss-20b",
    temperature=0.3,
)



prompt = create_prompt()


# ---- Sidebar: upload + process ----

with st.sidebar:

    st.header("Upload a document")

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "txt", "md", "docx"],
    )

    # ---- Process document ----

    process_clicked = st.button(
        "Process document",
        disabled=uploaded_file is None
    )

    # ---- Clear knowledge base ----

    clear_button = st.button(
        "🗑️ Clear knowledge base"
    )

    if clear_button:
        st.session_state.confirm_clear = True

    if st.session_state.confirm_clear:

        st.warning(
            "⚠️ This action cannot be undone."
        )

        confirmation = st.checkbox(
            "I understand and want to continue."
        )

        if confirmation:

            if st.button(
                "Yes, clear everything"
            ):

                try:

                    delete_vector_store(
                        st.session_state.vector_store
                    )

                    # Reset application state
                    st.session_state.vector_store = None
                    st.session_state.retriever = None
                    st.session_state.processed_files = []
                    st.session_state.messages = []
                    st.session_state.confirm_clear = False

                    st.success(
                        "✅ Knowledge base cleared successfully."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"❌ Failed to clear knowledge base: {e}"
                    )

    # ---- Process document ----

    if process_clicked and uploaded_file is not None:

        progress = st.progress(0)
        status = st.empty()
        temp_path = None

        try:

            # 1. Save uploaded file

            status.write(
                "📄 Preparing document..."
            )

            progress.progress(10)

            suffix = os.path.splitext(
                uploaded_file.name
            )[1]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
            ) as tmp_file:

                tmp_file.write(
                    uploaded_file.getvalue()
                )

                temp_path = tmp_file.name

            # 2. Load document

            status.write(
                "📖 Loading document..."
            )

            progress.progress(25)

            documents = load_document(
                temp_path
            )

            for doc in documents:

                doc.metadata["source"] = (
                    uploaded_file.name
                )

            # 3. Chunk document

            status.write(
                "✂️ Splitting document into chunks..."
            )

            progress.progress(45)

            chunks = chunk_documents(
                documents
            )

            # 4. Create embeddings + vector store

            status.write(
                "🧠 Creating embeddings and updating database..."
            )

            progress.progress(70)

            vector_store, added = create_vector_store(
                chunks
            )

            st.session_state.vector_store = vector_store

            # 5. Create retriever

            status.write(
                "🔎 Preparing retriever..."
            )

            progress.progress(90)

            st.session_state.retriever = (
                create_retriever(
                    vector_store
                )
            )

            # ---- Result ----

            if added:

                if uploaded_file.name not in (
                    st.session_state.processed_files
                ):

                    st.session_state.processed_files.append(
                        uploaded_file.name
                    )

                progress.progress(100)

                status.success(
                    f"✅ '{uploaded_file.name}' added! Ask away."
                )

            else:

                progress.progress(100)

                status.warning(
                    f"⚠️ '{uploaded_file.name}' "
                    "already exists in the knowledge base."
                )

        except Exception as e:

            status.error(
                f"❌ Failed to process document: {e}"
            )

        finally:

            if (
                temp_path is not None
                and os.path.exists(temp_path)
            ):

                os.remove(temp_path)

    # ---- Show processed documents ----

    if st.session_state.processed_files:

        st.caption(
            "Documents in knowledge base:"
        )

        for fname in st.session_state.processed_files:

            st.caption(
                f"• {fname}"
            )


# ---- Main chat area ----

if st.session_state.retriever is None:

    st.info(
        "Upload a document and click "
        "'Process document' to get started."
    )

else:

    # Show previous messages

    for msg in st.session_state.messages:

        with st.chat_message(
            msg["role"]
        ):

            st.markdown(
                msg["content"]
            )

    # Chat input

    user_question = st.chat_input(
        "Ask a question about your document..."
    )

    if user_question:

        # Keep only previous conversation messages
        history = st.session_state.messages.copy()

        # Generate answer using previous conversation
        with st.chat_message("user"):

            st.markdown(
                user_question
            )

        with st.chat_message("assistant"):

            with st.spinner(
                "Thinking..."
            ):

                answer, sources = ask_question(
                    user_question,
                    st.session_state.retriever,
                    prompt,
                    llm,
                    history
                )

                st.markdown(
                    answer
                )

                if sources:

                    st.caption(
                        "📄 Sources: "
                        + ", ".join(sources)
                    )

        # Save current user question after generating answer

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_question
            }
        )

        full_answer = answer

        if sources:

            full_answer += (
                "\n\n*Sources: "
                + ", ".join(sources)
                + "*"
            )

        # Save assistant answer

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_answer
            }
        )
