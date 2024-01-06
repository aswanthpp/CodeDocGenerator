
import sys
import os
import subprocess
import shutil
from langchain.text_splitter import Language
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain_community.chat_models import ChatOpenAI

def clone_repository(url, destination="tmp"):
    try:
        # Run the git clone command
        subprocess.run(["git", "clone", url, destination], check=True)
        print(f"Repository cloned successfully into {destination}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        return False

def delete_tmp_directory(file_path):
    try:
        # Check if the directory exists
        if os.path.exists(file_path):
            # Delete the directory and its contents
            shutil.rmtree(file_path)
            print(f"Temporary directory {file_path} deleted successfully.")
        else:
            print(f"Temporary directory {file_path} does not exist.")

        return True
    except Exception as e:
        print(f"Error deleting temporary directory: {e}")
        return False
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
    file_path="tmp"
    delete_tmp_directory(file_path)
    status=clone_repository(repo_path, file_path)
    if(status):
        documents = load_documents(file_path,language)
        texts = split_documents(documents,language)
        db = store_documents(texts)
        retriever = create_retriever(db)


        llm = ChatOpenAI(model_name="gpt-4")
        memory = ConversationSummaryMemory(llm=llm, memory_key="chat_history", return_messages=True)
        qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)
        return qa
    else:
        return None

def generate_response(qa,prompt):
    result = qa(prompt)

    return result["answer"]





