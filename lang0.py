##################################################
# Brian Lesko
# 2023-10-24
# Langchain / Retrieval Augmented Generation

# Import Langchain dependencies
import langchain
import openai
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Bring in streamlit for UI dev
import streamlit as st
# Bring in watsonx interface
# from watsonxlangchain import langchaininterface

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    openai.api_key = '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'
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

# Setup the app title
st.title('Ask an LLM')

# Setup a session state message variable to hold all the old messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display all the historical messages
for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['message'])

# Build a prompt input template to display the prompts
prompt = st.chat_input('Pass Your Prompt here')

# If the user hits enter then
if prompt:
    # Display the prompt
    st.chat_message('user').markdown(prompt)
    # Store the prompt in state
    st.session_state.messages.append({'role': 'user', 'message': prompt})
    # Build the response
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a writing expert that is concise yet interesting to read"},
        ]
        )
    response = completion.choices[0].message
    st.chat_message('assistant').markdown(response)
    # Store the response in state
    st.session_state.messages.append({'role': 'assistant', 'message': response})