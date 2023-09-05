import os
import sys
import atlassian
import openai
import pandas
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.document_loaders import ConfluenceLoader
from inspect import getfullargspec
from typing import List, Union

import constants

def is_str(v):
        return hasattr(v, 'lower')

def load_confluenceSpace (confluence_url, confluence_space_key, confluence_username, confluence_apikey):
    if (is_str(confluence_url) and is_str(confluence_username) and is_str(confluence_space_key) and (confluence_apikey)):
        loader = ConfluenceLoader (url=confluence_url, username=confluence_username, api_key=confluence_apikey)
        documents = loader. load (space_key=confluence_space_key,include_attachments=False)
        return documents


def loadConfluenceIndex():
    os.environ["OPENAI_API_KEY"] = constants.OPENAPIKEY
    os.environ["CONFLUENCE_API_KEY"] = constants.CONFLUENCEAPIKEY
    confluenceurl = constants.confluenceurl
    username = constants.username
    apikey = constants.CONFLUENCEAPIKEY
    confluence_space_keys = constants.confluence_space_keys
# Enable to save to disk & reuse the model (for repeated queries on the same data)
 

    documents = load_confluenceSpace( confluence_apikey=apikey, confluence_space_key=confluence_space_keys[0], confluence_url=confluenceurl, confluence_username=username)
    index = VectorstoreIndexCreator().from_documents(documents)
    for key in confluence_space_keys[1:]:
        documents = load_confluenceSpace( confluence_apikey=apikey, confluence_space_key=key, confluence_url=confluenceurl, confluence_username=username)
        index.vectorstore.add_documents(documents=documents)
    
    return index



   # documents = load_confluenceSpace( confluence_apikey=apikey, confluence_space_key=space_key, confluence_url=confluenceurl, confluence_username=username)


index = loadConfluenceIndex()
     
chain = ConversationalRetrievalChain.from_llm(
llm=ChatOpenAI(model="gpt-3.5-turbo"),
retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)
        




query = None
chat_history = []
while True:
    if not query:
        query = input("Prompt: ")
    if query in ['quit', 'q', 'exit']:
        sys.exit()
    result = chain({"question": query, "chat_history": chat_history})
    print(result['answer'])

    chat_history.append((query, result['answer']))
    query = None
