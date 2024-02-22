import os
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
# from langchain_community.vectorstores import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from constants import key, PineKey, PineEnv
from ScrapeData import start

os.environ['OPENAI_API_KEY'] = key
os.environ['PINECONE_API_KEY'] = PineKey
os.environ['PINECONE_ENV'] = PineEnv


def VctrUpload(query):
    text = start(query)
    Spltr = RecursiveCharacterTextSplitter(chunk_size = 1700, chunk_overlap = 170)
    Doc = Spltr.split_text(text)
    Embd = OpenAIEmbeddings()
    pc = Pinecone(api_key = PineKey)
    Idx = pc.Index("companydetail")
    Idx.upsert_items(["doc_" + str(i) for i in range(len(Doc))], Doc)
    # Idx = Pinecone.from_documents(Doc, Embd, index_name = "companydetail")


def rtrv(query, k=2):
    matchrslt = Idx.similarity_search(query, k=k)
    return matchrslt


VctrUpload("Canoo")