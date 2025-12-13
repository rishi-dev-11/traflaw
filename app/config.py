# import os
# from dotenv import load_dotenv

# load_dotenv()  # Load from .env

# # 🔐 Pinecone Config
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_ENV = os.getenv("PINECONE_ENV")
# PINECONE_INDEX = os.getenv("PINECONE_INDEX")

# # ☁️ AWS / Bedrock Config
# AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
# AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")



import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env

# 🔐 Pinecone Config
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_REGION = os.getenv("PINECONE_REGION")  # e.g., "us-east-1"
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

# ☁️ AWS / Bedrock Config
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
