#Comment for the syncronous processing of the user query
'''This module handles the chat functionality of the RAG system. 
It takes the user query, performs similarity search on the vector store to retrieve relevant documents, 
and then generates a response using the OpenAI language model based on the retrieved context. 
The response is then printed to the user.
It a typical Synchronous processing of the user query, 
where the system waits for the response to be generated before accepting the next user query.'''

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

INITIAL_SYSTEM_PROMPT = """You are a helpful assistant that provides information about the history of Odisha based on the documents provided. Answer the user's questions based on the relevant information retrieved from the documents with pagenumber. 
If you don't know the answer, say you don't know.
You should only answre based on the following context and navigate the user to the relevant page number in the document for more information.

Context:
"""

def similarity_search(query:str, url:str, collection:str, model:str):
    '''This module performs similarity search on the vector store(Qdrant) using the query and returns the relevant documents'''
    embedding_model = OpenAIEmbeddings(model=model)
    vector_db = QdrantVectorStore.from_existing_collection(
        url=url,
        collection_name=collection,
        embedding=embedding_model
    )
    results = vector_db.similarity_search(query=query)
    return results

def generate_response(system_prompt:str, user_query:str,llm_model:str):
    '''This module generates a response using the OpenAI language model based on the system prompt and user query'''
    client = OpenAI()
    response = client.chat.completions.create(
        model=llm_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    while True:
        user_query = input("Ask a question about the history of Odisha: ")
        if user_query.lower() in ["exit", "quit", "bye", "goodbye", "see you", "see you later",'']:
            print("Exiting the chat. Goodbye!")
            break
        relevant_results = similarity_search(user_query, URL, COLLECTION, EMBEDDING_MODEL)
        context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}" 
                             for result in relevant_results])
        SYSTEM_PROMPT = INITIAL_SYSTEM_PROMPT + context
        answer = generate_response(SYSTEM_PROMPT, user_query, LLM_MODEL)
        print("Answer: ", answer)