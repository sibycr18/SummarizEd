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

col1, col2 = st.columns([4, 1])

topic = col1.text_input("Enter the topic to summarize:")

st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
word_length = col2.radio(
    "Summary length:",
    ["Short", "Brief", "Medium", "Long"],
    index = 2,
    label_visibility = "hidden",
)

no_of_words = {
    "Short": 50,
    "Brief": 120,
    "Medium": 200,
    "Long": 400
}

query = f"""
Summarize the following topic in around {no_of_words[word_length]} words: "{topic}".
Use heading, bullet points, highlights etc. wherever necessary.
The result should not miss the main points of the topic.
"""

search_button = col1.button("Search", type="primary")
if search_button:
    collection = st.session_state.file_name
    st.subheader("", divider="gray")
    # st.subheader("Answer:")
    st.write(get_llm_response(query, collection))