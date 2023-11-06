import streamlit as st
import chromadb
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader

## Intitialization
# Intialize ChromaDB
@st.cache_resource
def init_db():
    db_client = chromadb.PersistentClient(path="./db")
    return db_client

# Initialize Embeddings
@st.cache_resource
def init_embedding():
    embeddings = HuggingFaceEmbeddings(model_name="infgrad/stella-base-en-v2")
    return embeddings

# Session states
db_client = st.session_state.db_client = init_db()
embeddings = st.session_state.embeddings = init_embedding()

# Already uploaded files
collections = st.session_state.db_client.list_collections()

## App Title
st.title("Summariz:orange[Ed] :gray[- PDF Summarizer]", )
# st.divider()
st.subheader("", divider="gray")    # maybe not be a proper way but i like this


# Display file uploader
uploaded_file = st.file_uploader("Upload a new PDF file", type=["pdf"])
# st.button("Process PDF", type="primary", disabled=True)

if uploaded_file is not None:
    file_name = uploaded_file.name
    # Read and display the content of the PDF file
    pdf_reader = PdfReader(uploaded_file)
    pdf_text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_text += page.extract_text()

    st.button("Process PDF", type="primary")

    # st.caption(f"File Name: {file_name}")

st.subheader("OR")

pdf_list = tuple(collection.name for collection in collections)
placeholder = "Select the PDF file..." if len(pdf_list) > 0 else "No PDFs uploaded"
selected_file = st.selectbox(
   "Already uploaded?",
   pdf_list,
   index=None,
   placeholder = placeholder,
)

# Print file content
if uploaded_file is not None:
    st.divider()
    st.header("PDF Content:")
    st.write(pdf_text)


##