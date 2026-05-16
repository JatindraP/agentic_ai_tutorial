from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import rag_utils as utils

load_dotenv()

PDF_PATH = utils.get_pdf_path("odia_history_document")
URL = utils.get_config("vectordb", "qdrant", "url")
COLLECTION = utils.get_config("vectordb", "qdrant", "collection","odisha_history_pdf")
MODEL = utils.get_config("embedding_model", "model_name")


def pdf_loader(file_path:str):
    '''This module to load the PDF using the Langchain PyPDFLoader and return the pages as a list of documents'''
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    return pages

def text_splitter(pages:list):
    '''This module splits the text into smaller chunks for processing'''
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
    chunks = splitter.split_documents(documents=pages)
    return chunks

def embeddings_vectorstore(chunks:list, url:str, collection:str, model:str):
    '''This module generates embeddings for the chunks using OpenAIEmbeddings
    Then stores the embeddings in a vector store(Qdrant) for later retrieval'''

    embedding_model = OpenAIEmbeddings(model=model)
    vector_store = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embedding_model,
        url=url,
        collection_name=collection
    )
    print("Embeddings generated and stored in Qdrant vector store successfully....")
    


if __name__ == "__main__":
    pages = pdf_loader(PDF_PATH)
    chunks = text_splitter(pages)
    embeddings_vectorstore(chunks, URL, COLLECTION, MODEL)