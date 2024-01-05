from bs4 import SoupStrainer

from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain import hub

import sys
import os

if len(sys.argv) != 2:
    print("Usage: python script.py <API_KEY>")
    sys.exit(1)

api_key = sys.argv[1]
os.environ["OPENAI_API_KEY"] = api_key

# 1. Load
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs={
        "parse_only": SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    },
)
docs = loader.load()
# print(len(docs[0].page_content))
# print(docs[0].page_content[:500])

# 2. Split
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)
# print(len(all_splits))
# print(all_splits[10].metadata)

# 3. Store
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())


# 4. Retrieve
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

retrieved_docs = retriever.get_relevant_documents(
    "What are the approaches to Task Decomposition?"
)
# print(len(retrieved_docs))
# print(retrieved_docs[0].page_content)

# 5. Generate 
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)



prompt = hub.pull("rlm/rag-prompt")
example_messages = prompt.invoke(
    {"context": "filler context", "question": "filler question"}
).to_messages()

print(example_messages[0].content)

