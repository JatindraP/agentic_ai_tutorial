from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI,Query
from client import rq_client
from queues import worker

app = FastAPI()

queue = rq_client.get_rq_queue()

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG system! Ask a question about the history of Odisha."}


@app.post("/chat")
def chat(query: str = Query(..., description="The user's question about the history of Odisha")):
    job = queue.enqueue(worker.process_query, query)
    return {"status": "enqueued", "job_id": job.id}

@app.get("/chat/results")
def get_result(job_id: str=Query(..., description="The ID of the job to fetch results for")):
    job = queue.fetch_job(job_id)
    return {"job_id": job_id, "result": job.result}