# import os
# import json
# import pinecone
# from sentence_transformers import SentenceTransformer
# from app.config import PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX

# # Initialize embedding model (384-dim)
# model = SentenceTransformer("all-MiniLM-L6-v2")

# # Initialize Pinecone connection
# pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
# index = pinecone.Index(PINECONE_INDEX)

# def embed_and_upsert(docs, namespace="traffic-law"):
#     """
#     Given a list of documents with 'text' or 'chunk' field, embed and upload to Pinecone.
#     """
#     vectors = []
#     for i, doc in enumerate(docs):
#         content = doc.get("text") or doc.get("chunk")
#         if not content:
#             continue
#         vector = model.encode(content).tolist()
#         metadata = {k: v for k, v in doc.items() if k not in ["chunk", "text"]}
#         vectors.append({
#             "id": f"doc-{namespace}-{i}",
#             "values": vector,
#             "metadata": {"text": content, **metadata}
#         })

#     # Upload in batches of 100
#     for i in range(0, len(vectors), 100):
#         batch = vectors[i:i+100]
#         index.upsert(vectors=batch, namespace=namespace)

# def query_pinecone(query, top_k=5, namespace="traffic-law"):
#     """
#     Embed the query and retrieve top-k similar documents from Pinecone.
#     """
#     query_vector = model.encode(query).tolist()
#     result = index.query(vector=query_vector, top_k=top_k, include_metadata=True, namespace=namespace)
#     return result["matches"]

# def clear_namespace(namespace="traffic-law"):
#     """
#     Clear all data from a given namespace (use before re-upload).
#     """
#     index.delete(delete_all=True, namespace=namespace)

# def save_vectors_to_jsonl(vectors, path):
#     """
#     Save embedding payloads to JSONL for inspection (optional).
#     """
#     with open(path, "w", encoding="utf-8") as f:
#         for item in vectors:
#             json.dump(item, f)
#             f.write("\n")




# import os
# import json
# import pinecone
# from sentence_transformers import SentenceTransformer
# from app.config import PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX

# # Initialize embedding model (384-dim)
# model = SentenceTransformer("all-MiniLM-L6-v2")

# # Connect to Pinecone
# pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
# index = pinecone.Index(PINECONE_INDEX)

# def embed_and_upsert(docs, namespace="traffic-law"):
#     """
#     Embed and upload list of documents to Pinecone.
#     Each doc should have 'text' or 'chunk', plus metadata.
#     """
#     vectors = []
#     for i, doc in enumerate(docs):
#         content = doc.get("text") or doc.get("chunk")
#         if not content:
#             continue
#         vector = model.encode(content).tolist()
#         metadata = {k: v for k, v in doc.items() if k not in ["chunk", "text"]}
#         vectors.append({
#             "id": f"doc-{namespace}-{i}",
#             "values": vector,
#             "metadata": {"text": content, **metadata}
#         })

#     for i in range(0, len(vectors), 100):
#         batch = vectors[i:i+100]
#         index.upsert(vectors=batch, namespace=namespace)

# def query_pinecone(query, top_k=5, namespace="traffic-law"):
#     """
#     Embed the query and retrieve top-K similar documents from Pinecone.
#     """
#     query_vector = model.encode(query).tolist()
#     result = index.query(
#         vector=query_vector,
#         top_k=top_k,
#         include_metadata=True,
#         namespace=namespace
#     )
#     return result["matches"]

# def clear_namespace(namespace="traffic-law"):
#     """
#     Clear a namespace in Pinecone (e.g. for clean re-upload).
#     """
#     index.delete(delete_all=True, namespace=namespace)

# def save_vectors_to_jsonl(vectors, path):
#     """
#     Save embedding payloads to JSONL (optional debugging).
#     """
#     with open(path, "w", encoding="utf-8") as f:
#         for item in vectors:
#             json.dump(item, f)
#             f.write("\n")





# import json
# import pinecone
# from pinecone import ServerlessSpec
# import uuid
# from sentence_transformers import SentenceTransformer
# from app.config import PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX

# # Initialize embedding model
# model = SentenceTransformer("all-MiniLM-L6-v2")

# # Connect to Pinecone (Legacy v2 syntax based on your code)
# # pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
# # index = pinecone.Index(PINECONE_INDEX)

# pc = Pinecone(api_key="your_key")  # No need to call init
# index = pc.Index("your_index")

# def embed_and_upsert(docs, namespace="traffic-law"):
#     """
#     Embed and upload list of documents to Pinecone.
#     """
#     vectors = []
#     print(f"   Embedding {len(docs)} chunks...")

#     for doc in docs:
#         content = doc.get("text") or doc.get("chunk")
#         if not content:
#             continue
        
#         # Generate vector
#         vector = model.encode(content).tolist()
        
#         # Separate metadata
#         metadata = {k: v for k, v in doc.items() if k not in ["chunk", "text", "id"]}
#         metadata["text"] = content # Ensure text is stored in metadata for retrieval later

#         # Generate a unique ID if one isn't provided
#         # This prevents overwriting previous data
#         doc_id = doc.get("id") or str(uuid.uuid4())

#         vectors.append({
#             "id": doc_id,
#             "values": vector,
#             "metadata": metadata
#         })

#     # Upsert in batches of 100
#     for i in range(0, len(vectors), 100):
#         batch = vectors[i:i+100]
#         try:
#             index.upsert(vectors=batch, namespace=namespace)
#             print(f"   Upserted batch {i} to {i+len(batch)}")
#         except Exception as e:
#             print(f"   Error upserting batch: {e}")

# # Keep your other functions (query_pinecone, etc.) as they are...
# def query_pinecone(query, top_k=5, namespace="traffic-law"):
#     query_vector = model.encode(query).tolist()
#     result = index.query(
#         vector=query_vector,
#         top_k=top_k,
#         include_metadata=True,
#         namespace=namespace
#     )
#     return result["matches"]



import json
import uuid
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from app.config import PINECONE_API_KEY, PINECONE_REGION, PINECONE_INDEX

# Initialize embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to Pinecone (new SDK)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX)

def embed_and_upsert(docs, namespace="traffic-law"):
    """
    Embed and upload list of documents to Pinecone.
    """
    vectors = []
    print(f"🔹 Embedding {len(docs)} chunks...")

    for doc in docs:
        content = doc.get("text") or doc.get("chunk")
        if not content:
            continue
        
        vector = model.encode(content).tolist()
        metadata = {k: v for k, v in doc.items() if k not in ["chunk", "text", "id"]}
        metadata["text"] = content
        doc_id = doc.get("id") or str(uuid.uuid4())

        vectors.append({
            "id": doc_id,
            "values": vector,
            "metadata": metadata
        })

    for i in range(0, len(vectors), 100):
        batch = vectors[i:i+100]
        try:
            index.upsert(vectors=batch, namespace=namespace)
            print(f"✅ Upserted batch {i} to {i+len(batch)}")
        except Exception as e:
            print(f"❌ Error upserting batch: {e}")

def query_pinecone(query, top_k=5, namespace="traffic-law"):
    query_vector = model.encode(query).tolist()
    result = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )
    return result["matches"]
