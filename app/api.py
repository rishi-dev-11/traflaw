# from fastapi import FastAPI
# from pydantic import BaseModel
# from app.retriever import query_pinecone
# from app.generator import generate_answer

# app = FastAPI(title="Indian Traffic Law Assistant")

# class QueryRequest(BaseModel):
#     query: str
#     top_k: int = 5

# class Citation(BaseModel):
#     text: str
#     type: str | None = None
#     section: str | None = None
#     case_id: str | None = None

# class QueryResponse(BaseModel):
#     query: str
#     answer: str
#     citations: list[Citation]

# @app.post("/ask", response_model=QueryResponse)
# async def ask_question(request: QueryRequest):
#     """
#     Accepts a legal question and returns an AI-generated answer
#     along with relevant citations from the knowledge base.
#     """
#     # Step 1: Vector search
#     retrieved_docs = query_pinecone(request.query, top_k=request.top_k)

#     # Step 2: Answer generation
#     answer = generate_answer(request.query, retrieved_docs)

#     # Step 3: Return structured response
#     return {
#         "query": request.query,
#         "answer": answer.strip(),
#         "citations": [doc["metadata"] for doc in retrieved_docs]
#     }






from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from app.retriever import query_pinecone
from app.generator import generate_answer

app = FastAPI(
    title="Indian Traffic Law Assistant API",
    description="RAG-based API using Pinecone and Claude 3 Sonnet",
    version="1.0.0"
)

# --- CORS Configuration ---
# Allows your API to be called from web browsers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class SourceDocument(BaseModel):
    """
    Represents a chunk of text retrieved from Pinecone.
    Matches the metadata structure created in loader.py.
    """
    source: str = Field(..., description="The filename or source ID")
    text: str = Field(..., description="The actual legal text content")
    category: Optional[str] = Field(None, description="Type of doc: statute, report, etc.")
    score: Optional[float] = Field(None, description="Similarity score from Vector DB")

class QueryResponse(BaseModel):
    query: str
    answer: str
    sources: List[SourceDocument]

# --- Endpoints ---

@app.get("/")
async def root():
    return {"status": "ok", "message": "Traffic Law AI is running"}

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """
    Accepts a legal question and returns an AI-generated answer
    along with relevant citations (sources) from the knowledge base.
    """
    try:
        # Step 1: Vector search (Retrieve)
        print(f"🔍 Searching for: {request.query}")
        raw_matches = query_pinecone(request.query, top_k=request.top_k)

        # Step 2: Answer generation (Generate)
        # Note: raw_matches is a list of Pinecone dictionaries
        answer = generate_answer(request.query, raw_matches)

        # Step 3: Format sources for the response
        formatted_sources = []
        for match in raw_matches:
            metadata = match.get("metadata", {})
            formatted_sources.append(
                SourceDocument(
                    source=metadata.get("source", "Unknown Source"),
                    text=metadata.get("text", ""),
                    category=metadata.get("category", "general"),
                    score=match.get("score", 0.0)
                )
            )

        return {
            "query": request.query,
            "answer": answer.strip(),
            "sources": formatted_sources
        }

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))