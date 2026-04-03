import sys
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.query import query_pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def handle_query(request: QueryRequest):
    answer = query_pipeline(request.query)
    return {"answer": answer}

if __name__ == "__main__":

    query = "how to lower my risk of prediabetes？"

    answer = query_pipeline(query)

    print("Answer:")
    print(answer)