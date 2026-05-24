from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
import rag_utils as utils
from dotenv import load_dotenv
load_dotenv()

URL = utils.get_config("vectordb", "qdrant", "url")
COLLECTION = utils.get_config("vectordb", "qdrant", "collection","odisha_history_pdf")
EMBEDDING_MODEL = utils.get_config("embedding_model", "model_name")
LLM_MODEL = utils.get_config("llm_model", "openai_model_name")


embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)
vector_db = QdrantVectorStore.from_existing_collection(
        url=URL,
        collection_name=COLLECTION,
        embedding=embedding_model
    )

INITIAL_SYSTEM_PROMPT = """You are a helpful assistant that provides information about the history of Odisha based on the documents provided. Answer the user's questions based on the relevant information retrieved from the documents with pagenumber. 
If you don't know the answer, say you don't know.
You should only answre based on the following context and navigate the user to the relevant page number in the document for more information.

Context:
"""

def process_query(query:str):
    print(f"Searching chunks for : {query} ! ...")
    results = vector_db.similarity_search(query=query)


    print("Preparing system prompt for the LLM model with the retrieved context ...")
    context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}" 
                             for result in results])
    SYSTEM_PROMPT = INITIAL_SYSTEM_PROMPT + context

    print("Generating response using the LLM model ...")
    client = OpenAI()
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content