##################################################
# Brian Lesko
# 2023-11-2
# In this Low code UI, we implement RAG, retrieval augmented generation, with an LLM, to answer questions from a document
# Practice Coding

# Import Langchain dependencies
from langchain.document_loaders import PyPDFLoader 
from langchain.indexes import VectorstoreIndexCreator 
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings 
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Import Streamlit dependencies
import streamlit as st

# Import other dependencies
import openai

##################################################
# Load the document
# chunk the document and load it into a vectorstore
@st.cache_resource 
def load_pdf():
    # Update PDF name here to whatever you Like
    file_name = 'lease.pdf'
    loaders = [PyPDFLoader(file_name)]
    # Create index - aka vector database
    index = VectorstoreIndexCreator(
        embedding = HuggingFaceEmbeddings (model_name='all-MiniLM-L12-v2'),
        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=100, 
            chunk_overlap=20,
            length_function=len,
            is_separator_regex= False
            )
    ).from_loaders(loaders)
    return index

##################################################
# rework 

text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=100, 
    chunk_overlap=20,
    length_function=len,
    is_separator_regex= False
    )
data = text_splitter.split_text(open('lease.pdf').read())

# Store embeddings in a vectorstore chromaDB
from langchain.vectorstores import Chroma 
from langchain.embeddings import OpenAIEmbeddings
embeddings = OpenAIEmbeddings ()

store = Chroma.from_documents(
    embeddings,
    ids = [f"{item.metadata['source']}-{index}" for index, item in enumerate(data)],
    collection_name="Wimbledon-Embeddings",
    persist_directory='db',
)
store.persist()

# Template and Question
from langchain.chains import RetrievalQA 
from langchain.prompts import PromptTemplate 
from langchain.chat_models import ChatOpenAI
import pprint

template = """You are a bot that answers questions using the context provided. If you need to make an assumption you must say so."
｛context｝
Question: {question}"""

PROMPT = PromptTemplate(
    template=template, input_variables=["context", "question"]
)

qa_with_source = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=store.as_retriever(),
    chain_type_kwargs={"prompt": PROMPT, },
    return_source_documents=True,
)
# end rework
####################################################

# load her up
index = load_pdf()

####################################################
# API Key
from api_key import openai_api_key
from about_sidebar import about

openai_api_key_file = openai_api_key

with st.sidebar:
    about()
    st.write('  ') 
    st.markdown("""---""")
    openai_api_key = st.text_input("# OpenAI API Key", key="chatbot_api_key", type="password")
    col1, col2 = st.columns([1,5], gap="medium")
    with col2:
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

    # Get an open ai key, the company behind the first popular LLM, GPT-3
    if not openai_api_key and not openai_api_key_file:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    if openai_api_key_file:
        openai.api_key = openai_api_key_file
        openai_api_key = openai_api_key_file

####################################################
# create an llm using langchain openai wrapper
from langchain.llms import OpenAI
llm = OpenAI(model_name = 'gpt-4', max_tokens = 100, temperature = 0.9,openai_api_key = openai_api_key)

# create the qa chain 
chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type = 'stuff',
    retriever=index.vectorstore.as_retriever(),
    input_key='question')

####################################################
# initialize the chat history
st.title("Retreival Augmented Generation with an LLM")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display all the historical messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

####################################################
# Call the chatbot
if prompt := st.chat_input("Write a message"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = chain.run(prompt)
    # openai.ChatCompletion.create(model="gpt-4", messages=st.session_state.messages)
    #msg = response.choices[0].message
    st.session_state.messages.append({'role' :'assistant', 'content' :response})
    st.chat_message('assistant').markdown(response)

##################################################
# Related topics: OpenAI Generative Transformers, AI, Streamlit, Chatbot, Python, Low Code, UI, Low code UI, Large Language model