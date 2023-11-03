##################################################
# rework 

from langchain.text_splitter import RecursiveCharacterTextSplitter
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

print(qa_with_source("What is the term of the lease?"))