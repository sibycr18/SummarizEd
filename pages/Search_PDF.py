import streamlit as st
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import Ollama
from langchain.vectorstores import Chroma

db_client = st.session_state.db_client
embeddings = st.session_state.embeddings

def create_agent_chain():
    llm = Ollama(model="mistral")
    chain = load_qa_chain(llm, chain_type="stuff")
    return chain


def get_llm_response(query, collection):
    vectordb = Chroma(
        client = db_client,
        collection_name = collection,
        embedding_function = embeddings,
    )
    chain = create_agent_chain()
    matching_docs = vectordb.similarity_search(query)
    answer = chain.run(input_documents=matching_docs, question=query)
    return answer


## App Title
st.title("Summariz:orange[Ed] :gray[- PDF Summarizer]")
st.subheader("", divider="gray")

# Columns for inputs
col1, col2 = st.columns([4, 1])

# Save topic entered in session state
topic = st.session_state.topic
topic = col1.text_input("Enter the topic to summarize:", value = topic)
st.session_state.topic = topic

# Radio buttons for word limit
word_length = col2.radio(
    "Word limit:",
    ["No limit", "Short", "Brief", "Medium", "Long"],
    index = 0
)

# Query Formatting
if word_length == "No limit":
    query = f"""
    Summarize the following topic: "{topic}".
    Use heading, bullet points, highlights etc. wherever necessary.
    The result should not miss the main points of the topic but also not include unecessary sentences.
    """
else:
    no_of_words = {
        "Short": 50,
        "Brief": 120,
        "Medium": 200,
        "Long": 400
    }
    query = f"""
    Summarize the following topic in around {no_of_words[word_length]} words: "{topic}".
    Use heading, bullet points, highlights etc. wherever necessary.
    The result should not miss the main points of the topic but also not include unecessary sentences.
    """

# Create search button
search_button = col1.button("Search", type="primary")

# Check if search button is clicked
if search_button:
    # Show loading spinner while summarizing
    with st.spinner("Summarising the topic. Please wait..."):
        # Get the selected PDF collection
        collection = st.session_state.file_name
        # Check if a PDF file is selected
        if collection == None:
            st.warning("Please select or upload a PDF file first.")
        else:
            # Get the response text from LLM model
            response_text = get_llm_response(query, collection)
            st.subheader("Answer", divider="gray")
            # Display the response text
            st.write(str(response_text))
