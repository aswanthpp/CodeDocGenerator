
import sys
import os

from langchain.text_splitter import Language
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain_community.chat_models import ChatOpenAI


def load_documents(repo_path, language):
    if language.lower() == 'python':
        suffixes = [".py"]
        parser = LanguageParser(language=Language.PYTHON, parser_threshold=500)
    elif language.lower() == 'java':
        suffixes = [".java"]
        parser = LanguageParser(language=Language.JAVA, parser_threshold=500)
    else:
        raise ValueError("Unsupported language")

    loader = GenericLoader.from_filesystem(
        repo_path,
        glob="**/*",
        suffixes=suffixes,
        exclude=["**/non-utf8-encoding.py"],
        parser=parser,
    )
    documents = loader.load()
    return documents

def split_documents(documents, language):
    if language.lower() == 'python':
        splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
        )
    elif language.lower() == 'java':
        splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.JAVA, chunk_size=2000, chunk_overlap=200
        )
    else:
        raise ValueError("Unsupported language")

    texts = splitter.split_documents(documents)
    return texts


def store_documents(texts):
    db = Chroma.from_documents(texts, OpenAIEmbeddings(disallowed_special=()))
    return db

def create_retriever(db):
    retriever = db.as_retriever(
    search_type="mmr",  # Also test "similarity"
    search_kwargs={"k": 8},
    )
    
    return retriever

def update_data_store(repo_path, language):
    documents = load_documents(repo_path,language)
    texts = split_documents(documents,language)
    db = store_documents(texts)
    retriever = create_retriever(db)


    llm = ChatOpenAI(model_name="gpt-4")
    memory = ConversationSummaryMemory(
    llm=llm, memory_key="chat_history", return_messages=True
)
    qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)
    return qa

def generate_response(qa,prompt):
    result = qa(prompt)

    return result["answer"]

# if(__name__=='__main__'):
#     if len(sys.argv) != 2:
#      print("Usage: python script.py <API_KEY>")
#      sys.exit(1)

#     api_key = sys.argv[1]
#     os.environ["OPENAI_API_KEY"] = api_key

#     repo_path="~/Learning/SelfLearning/GenAI/CodeDocGenerator/SimplePrompts"
#     language="PYTHON"
    
#     qa = update_data_store(repo_path,language)
#     response=generate_response(qa)
#     print(response)





