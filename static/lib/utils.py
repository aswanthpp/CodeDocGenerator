
import os
import shutil
from langchain.text_splitter import Language
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI
from git import InvalidGitRepositoryError, Repo
from langchain_community.document_loaders import GitLoader
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

file_path="source_code"
persist_directory="chroma_db"
embedding_function=OpenAIEmbeddings(disallowed_special=())

class LangChainCodeLoder:
    def __init__(self,qa):
        self.qa=qa

    def delete_tmp_directory(self):
        try:
            # Check if the directory exists
            if os.path.exists(file_path):
                # Delete the directory and its contents
                shutil.rmtree(file_path)
            return True
        except Exception as e:
            print(f"Got Exception while deleting temporary directory: {e}")
            return False
        
    def get_document_from_git(self, url):
        try:
            print("Cloning Started.......")
            repo = Repo.clone_from(url, to_path=file_path)
            branch =repo.head.reference
            print("Cloning Completed.......")
            
            print("GitLoader Started.......")
            loader = GitLoader(repo_path=file_path, branch=branch)
            documents=loader.load()
            print("GitLoader Completed.......")

            print("Branch: ", branch)
            print("Length of documents: ",len(documents))
            return documents
        except InvalidGitRepositoryError as e:
            print(f"Error: Invalid Git repository - {e}")
            return None
        except Exception as e:
            print(f"Got Excpetion while loading document: {e}")
            return None
                 
    def persist_embeddeings_to_vector_db(self,documents,language):
        try: 
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

            db = Chroma.from_documents(texts, embedding_function,persist_directory=persist_directory)
            db.persist()
            db = None
            self.delete_tmp_directory()
            response_json={
            'status': 'Success',
            'message': "Loading Codebase is Completed"
            }
            return response_json
        except Exception as e:
            print(f"Got Expcetion while persisting embeddings: {e}")
            return None
        
    def create_retirver(self):
        try: 
            print("creating retreiver by fetching from chroma db")
            db = Chroma(persist_directory=persist_directory, 
                    embedding_function=embedding_function)

            retriever = db.as_retriever(
                search_type="mmr",  # Also test "similarity"
                search_kwargs={"k": 8},
                )
            return retriever
        except Exception as e:
            print(f"Got Expcetion while persisting embeddings: {e}")
            return None
        
    def get_response_from_open_ai_llm_chain(self,retriever, prompt):
        try:
            print("creating conversation chain by combining llm( GPT-4) with retriever")
            llm = ChatOpenAI(model_name="gpt-4")
            memory = ConversationSummaryMemory(llm=llm, memory_key="chat_history", return_messages=True)
            qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)
            result = qa(prompt)
            if("answer" in result):
                return result["answer"]
            else:
                return None
        except Exception as e:
            print(f"Got Expcetion while Getting Response from Open AI, GPT-4: {e}")
            return None

    def get_response_from_llm_chain(self,retriever,prompt):

        try:
            print("creating conversation chain by combining llm with retriever")
            qa = RetrievalQA.from_chain_type(llm=OpenAI(), 
                                    chain_type="stuff", 
                                    retriever=retriever, 
                                    return_source_documents=False)
            result = qa(prompt)
            if("result" in result):
                return result["result"]
            else:
                return None
        except Exception as e:
            print(f"Got Expcetion while Getting response from LLM: {e}")
            return None
        
        
        
    def update_data_store(self,repo_path, language):
        if(not self.delete_tmp_directory()):
           response_json={
                    'status': 'Failure',
                    'message': "Exception while cleaning up older documents"
                }
           return response_json
        
        documents=self.get_document_from_git(repo_path)
        if(documents==None):
            response_json={
                    'status': 'Failure',
                    'message': "Please Enter valid github repo, which is public"
                }
            return response_json

        try:
            return self.persist_embeddeings_to_vector_db(documents,language)
        except Exception as e:
            print(f"Got Expcetion while Persisting the documents to Chroma DB: {e}")
            response_json={
            'status': 'Failure',
            'message': "Exception while loading codebase to store"
            }
            return response_json
    
    
        
    def generate_response(self,prompt):
        try:
            retriver=self.create_retirver()
            if(retriver is None):
                return None
            return self.get_response_from_llm_chain(retriver, prompt)
        except Exception as e:
            print(f"Got Expcetion while Getting Response: {e}")
            return None

