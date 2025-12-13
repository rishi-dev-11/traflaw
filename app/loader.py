# import fitz  # PyMuPDF
# from pathlib import Path

# def extract_sections_from_pdf(pdf_path):
#     """
#     Extracts section-wise content from a legal PDF file.
#     Returns a list of dictionaries with 'section' and 'text'.
#     """
#     doc = fitz.open(pdf_path)
#     sections = []
#     current_section = ""
#     current_text = ""

#     for page in doc:
#         for line in page.get_text().split("\n"):
#             if line.lower().startswith("section") or line.strip().isdigit():
#                 if current_section:
#                     sections.append({"section": current_section.strip(), "text": current_text.strip()})
#                 current_section = line.strip()
#                 current_text = ""
#             else:
#                 current_text += " " + line.strip()

#     if current_section:
#         sections.append({"section": current_section.strip(), "text": current_text.strip()})

#     return sections

# def chunk_case_file(filepath, chunk_size=350):
#     """
#     Reads a case law TXT file and chunks its content into segments of ~chunk_size words.
#     Returns a list of strings.
#     """
#     with open(filepath, 'r', encoding='utf-8') as f:
#         text = f.read().replace('\n', ' ')
#     words = text.split()
#     return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# def format_chunks(case_id, chunks):
#     """
#     Formats text chunks into dictionaries with case_id and metadata.
#     Returns a list of dictionaries ready for Pinecone.
#     """
#     return [{"case_id": case_id, "type": "case", "chunk": chunk} for chunk in chunks]

# def load_all_cases(case_dir):
#     """
#     Loads and formats all TXT files in a given case law directory.
#     Returns a list of all chunked documents.
#     """
#     all_docs = []
#     for txt_path in Path(case_dir).glob("*.txt"):
#         case_id = txt_path.stem.upper()
#         chunks = chunk_case_file(txt_path)
#         formatted = format_chunks(case_id, chunks)
#         all_docs.extend(formatted)
#     return all_docs





# import os
# import fitz  # PyMuPDF
# from pathlib import Path
# from sentence_transformers import SentenceTransformer
# from dotenv import load_dotenv
# import pinecone

# load_dotenv()

# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_ENV = os.getenv("PINECONE_ENV")
# PINECONE_INDEX = os.getenv("PINECONE_INDEX")

# model = SentenceTransformer("all-MiniLM-L6-v2")

# pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
# index = pinecone.Index(PINECONE_INDEX)

# def extract_sections_from_pdf(pdf_path):
#     doc = fitz.open(pdf_path)
#     sections = []
#     current_section = ""
#     current_text = ""

#     for page in doc:
#         for line in page.get_text().split("\n"):
#             if line.lower().startswith("section") or line.strip().isdigit():
#                 if current_section:
#                     sections.append({"section": current_section.strip(), "text": current_text.strip()})
#                 current_section = line.strip()
#                 current_text = ""
#             else:
#                 current_text += " " + line.strip()

#     if current_section:
#         sections.append({"section": current_section.strip(), "text": current_text.strip()})

#     return sections

# def chunk_case_file(filepath, chunk_size=350):
#     with open(filepath, 'r', encoding='utf-8') as f:
#         text = f.read().replace('\n', ' ')
#     words = text.split()
#     return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# def format_chunks(case_id, chunks):
#     return [{"case_id": case_id, "type": "case", "chunk": chunk} for chunk in chunks]

# def load_all_cases(case_dir):
#     all_docs = []
#     for txt_path in Path(case_dir).glob("*.txt"):
#         case_id = txt_path.stem.upper()
#         chunks = chunk_case_file(txt_path)
#         formatted = format_chunks(case_id, chunks)
#         all_docs.extend(formatted)
#     return all_docs

# def upload_to_pinecone(documents):
#     for i, doc in enumerate(documents):
#         content = doc["chunk"] if doc["type"] == "case" else doc["text"]
#         embedding = model.encode(content).tolist()
#         index.upsert([{
#             "id": f"{doc['type']}_{i}",
#             "values": embedding,
#             "metadata": {
#                 "text": content,
#                 "type": doc["type"],
#                 "case_id": doc.get("case_id", None),
#                 "section": doc.get("section", None)
#             }
#         }])

# def process_and_upload_all(pdf_path, case_dir):
#     pdf_sections = extract_sections_from_pdf(pdf_path)
#     upload_to_pinecone([{"type": "statute", **sec} for sec in pdf_sections])

#     case_docs = load_all_cases(case_dir)
#     upload_to_pinecone(case_docs)






# import fitz  # PyMuPDF
# from pathlib import Path
# from app.retriever import embed_and_upsert

# def extract_sections_from_pdf(pdf_path):
#     """
#     Extracts section-wise content from a legal PDF file.
#     Returns a list of dicts with 'section' and 'text'.
#     """
#     doc = fitz.open(pdf_path)
#     sections = []
#     current_section = ""
#     current_text = ""

#     for page in doc:
#         for line in page.get_text().split("\n"):
#             if line.lower().startswith("section") or line.strip().isdigit():
#                 if current_section:
#                     sections.append({"section": current_section.strip(), "text": current_text.strip()})
#                 current_section = line.strip()
#                 current_text = ""
#             else:
#                 current_text += " " + line.strip()

#     if current_section:
#         sections.append({"section": current_section.strip(), "text": current_text.strip()})

#     return sections

# def chunk_case_file(filepath, chunk_size=350):
#     """
#     Reads a case law TXT file and chunks it into ~chunk_size word segments.
#     Returns a list of strings.
#     """
#     with open(filepath, 'r', encoding='utf-8') as f:
#         text = f.read().replace('\n', ' ')
#     words = text.split()
#     return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# def format_chunks(case_id, chunks):
#     """
#     Formats chunks with case_id and type metadata.
#     """
#     return [{"case_id": case_id, "type": "case", "chunk": chunk} for chunk in chunks]

# def load_all_cases(case_dir):
#     """
#     Loads and formats all TXT case law files from directory.
#     Returns a list of chunked docs.
#     """
#     all_docs = []
#     for txt_path in Path(case_dir).glob("*.txt"):
#         case_id = txt_path.stem.upper()
#         chunks = chunk_case_file(txt_path)
#         formatted = format_chunks(case_id, chunks)
#         all_docs.extend(formatted)
#     return all_docs

# def process_and_upload_all(pdf_path, case_dir):
#     """
#     Extracts + embeds both Act PDF and court cases, uploads to Pinecone.
#     """
#     print("📘 Extracting sections from Motor Vehicles Act...")
#     act_sections = extract_sections_from_pdf(pdf_path)
#     embed_and_upsert(act_sections, namespace="mva")

#     print("📄 Loading and chunking court case files...")
#     case_docs = load_all_cases(case_dir)
#     embed_and_upsert(case_docs, namespace="cases")

#     print("✅ All data uploaded to Pinecone.")



# import fitz  # PyMuPDF
# import os
# from pathlib import Path
# from app.retriever import embed_and_upsert

# # --- Configuration ---
# # Define paths relative to this script (app/loader.py)
# BASE_DIR = Path(__file__).parent.parent
# DATA_DIR = BASE_DIR / "data" / "Data"

# AILA_DIR = DATA_DIR / "AILA_2019_dataset"
# ROAD_ACCIDENT_DIR = DATA_DIR / "Road Accident"

# CHUNK_SIZE = 500  # Number of words per chunk
# CHUNK_OVERLAP = 50 # Overlap to maintain context

# def get_text_chunks(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
#     """
#     Splits text into overlapping chunks of words.
#     """
#     words = text.split()
#     chunks = []
#     for i in range(0, len(words), chunk_size - overlap):
#         chunk = " ".join(words[i:i + chunk_size])
#         chunks.append(chunk)
#     return chunks

# def process_pdf_file(filepath, category):
#     """
#     Reads a PDF, extracts text page-by-page, and chunks it.
#     Returns a list of dicts ready for Pinecone.
#     """
#     doc = fitz.open(filepath)
#     processed_data = []
    
#     filename = filepath.name
#     print(f"   Processing PDF: {filename}...")

#     full_text = ""
#     for page_num, page in enumerate(doc):
#         full_text += page.get_text() + " "
    
#     # Create chunks from the full text of the document
#     # (Alternatively, you can chunk page by page if documents are huge)
#     chunks = get_text_chunks(full_text)
    
#     for i, chunk in enumerate(chunks):
#         processed_data.append({
#             "text": chunk,
#             "metadata": {
#                 "source": filename,
#                 "category": category,
#                 "type": "pdf",
#                 "chunk_id": i
#             }
#         })
        
#     return processed_data

# def process_txt_file(filepath, category):
#     """
#     Reads a TXT file and chunks it.
#     Returns a list of dicts ready for Pinecone.
#     """
#     filename = filepath.name
#     # print(f"   Processing TXT: {filename}...")
    
#     try:
#         with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
#             text = f.read().replace('\n', ' ')
            
#         chunks = get_text_chunks(text)
#         processed_data = []
        
#         for i, chunk in enumerate(chunks):
#             processed_data.append({
#                 "text": chunk,
#                 "metadata": {
#                     "source": filename,
#                     "category": category,
#                     "type": "text",
#                     "chunk_id": i
#                 }
#             })
#         return processed_data
        
#     except Exception as e:
#         print(f"Error reading {filename}: {e}")
#         return []

# def load_and_upload_all():
#     """
#     Main function to traverse directories, process files, and upload to Pinecone.
#     """
#     all_documents = []

#     # --- 1. Process Road Accident PDFs ---
#     print("📂 Loading Road Accident Reports & Acts...")
#     if ROAD_ACCIDENT_DIR.exists():
#         for pdf_file in ROAD_ACCIDENT_DIR.glob("*.pdf"):
#             # Distinguish between the Act and the Reports
#             category = "statute" if "Act" in pdf_file.name else "report"
#             docs = process_pdf_file(pdf_file, category=category)
#             all_documents.extend(docs)
#     else:
#         print(f"⚠️ Warning: Directory not found: {ROAD_ACCIDENT_DIR}")

#     # --- 2. Process AILA Statutes (TXT) ---
#     print("📂 Loading AILA Statutes...")
#     statutes_dir = AILA_DIR / "Object_statutes"
#     if statutes_dir.exists():
#         for txt_file in statutes_dir.glob("*.txt"):
#             docs = process_txt_file(txt_file, category="statute")
#             all_documents.extend(docs)
#     else:
#         print(f"⚠️ Warning: Directory not found: {statutes_dir}")

#     # --- 3. Process AILA Case Docs (TXT) ---
#     print("📂 Loading AILA Case Documents...")
#     cases_dir = AILA_DIR / "Object_casedocs"
#     if cases_dir.exists():
#         for txt_file in cases_dir.glob("*.txt"):
#             docs = process_txt_file(txt_file, category="case_law")
#             all_documents.extend(docs)
#     else:
#         print(f"⚠️ Warning: Directory not found: {cases_dir}")

#     # --- 4. Upload to Pinecone ---
#     print(f"🚀 Preparing to upload {len(all_documents)} chunks to Pinecone...")
    
#     # We define a generic formatting function effectively mapping our data to what embed_and_upsert expects
#     # Assuming embed_and_upsert expects a list of dictionaries with specific keys
#     # If your embed_and_upsert expects just text and metadata separately, adjust below.
    
#     # We will upload in batches to avoid hitting API limits
#     batch_size = 100
#     for i in range(0, len(all_documents), batch_size):
#         batch = all_documents[i:i+batch_size]
#         print(f"   Uploading batch {i} to {i+len(batch)}...")
        
#         # Calling your existing retriever function
#         # Ensure embed_and_upsert handles the list structure: [{'text': '...', 'metadata': {...}}, ...]
#         embed_and_upsert(batch, namespace="legal_knowledge_base")

#     print("✅ All data uploaded successfully!")

# if __name__ == "__main__":
#     load_and_upload_all()




import fitz  # PyMuPDF
import os
from pathlib import Path
from app.retriever import embed_and_upsert

# --- CONFIGURATION ---
# Dynamically find the path: app/../data/Data
BASE_DIR = Path(__file__).parent.parent
DATA_ROOT = BASE_DIR / "data" / "Data"

# Directories based on your screenshot
DIRS = {
    "statutes": DATA_ROOT / "AILA_2019_dataset" / "Object_statutes",
    "cases": DATA_ROOT / "AILA_2019_dataset" / "Object_casedocs",
    "reports": DATA_ROOT / "Road Accident"
}

# Chunking Settings
CHUNK_SIZE = 400     # Words per chunk
CHUNK_OVERLAP = 50   # Overlap to keep context between chunks

def get_overlapping_chunks(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Splits text into overlapping chunks.
    """
    words = text.split()
    if not words:
        return []
        
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk_words = words[i:i + chunk_size]
        chunk_text = " ".join(chunk_words)
        chunks.append(chunk_text)
        
        # Stop if we've reached the end
        if i + chunk_size >= len(words):
            break
            
    return chunks

def process_pdf(filepath, category):
    """Extracts text from PDF."""
    try:
        doc = fitz.open(filepath)
        full_text = ""
        for page in doc:
            full_text += page.get_text() + " "
        
        chunks = get_overlapping_chunks(full_text)
        formatted_docs = []
        
        for i, chunk in enumerate(chunks):
            formatted_docs.append({
                "text": chunk,
                "source": filepath.name,
                "category": category, # e.g., 'report' or 'act'
                "type": "pdf"
            })
        return formatted_docs
    except Exception as e:
        print(f"❌ Error reading PDF {filepath.name}: {e}")
        return []

def process_txt(filepath, category):
    """Extracts text from TXT."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read().replace('\n', ' ')
            
        chunks = get_overlapping_chunks(text)
        formatted_docs = []
        
        for i, chunk in enumerate(chunks):
            formatted_docs.append({
                "text": chunk,
                "source": filepath.name,
                "category": category, # e.g., 'case' or 'statute'
                "type": "text"
            })
        return formatted_docs
    except Exception as e:
        print(f"❌ Error reading TXT {filepath.name}: {e}")
        return []

def run_ingestion():
    print(f"🚀 Starting ingestion from: {DATA_ROOT}")
    
    # 1. Process AILA Statutes (.txt)
    if DIRS["statutes"].exists():
        print(f"\n📂 Processing Statutes from {DIRS['statutes'].name}...")
        all_statutes = []
        for file in DIRS["statutes"].glob("*.txt"):
            all_statutes.extend(process_txt(file, category="statute"))
        
        if all_statutes:
            embed_and_upsert(all_statutes, namespace="traffic-law")
            print(f"✅ Uploaded {len(all_statutes)} statute chunks.")

    # 2. Process AILA Cases (.txt)
    if DIRS["cases"].exists():
        print(f"\n📂 Processing Cases from {DIRS['cases'].name}...")
        # Processing cases in batches to save memory
        current_batch = []
        for file in DIRS["cases"].glob("*.txt"):
            docs = process_txt(file, category="case_law")
            current_batch.extend(docs)
            
            # Upload every 500 chunks to avoid memory overflow
            if len(current_batch) >= 500:
                embed_and_upsert(current_batch, namespace="traffic-law")
                current_batch = []
        
        # Upload remaining
        if current_batch:
            embed_and_upsert(current_batch, namespace="traffic-law")

    # 3. Process Road Accident PDFs (.pdf)
    if DIRS["reports"].exists():
        print(f"\n📂 Processing PDF Reports from {DIRS['reports'].name}...")
        all_pdfs = []
        for file in DIRS["reports"].glob("*.pdf"):
            # Distinguish between the Act and the Yearly Reports
            cat = "statute" if "Act" in file.name else "report"
            all_pdfs.extend(process_pdf(file, category=cat))
            
        if all_pdfs:
            embed_and_upsert(all_pdfs, namespace="traffic-law")
            print(f"✅ Uploaded {len(all_pdfs)} PDF chunks.")

    print("\n🎉 Ingestion Complete.")

if __name__ == "__main__":
    run_ingestion()