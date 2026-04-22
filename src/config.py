import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Model Configuration
# API kalitingiz qo'llab-quvvatlaydigan eng zamonaviy model
MODEL_NAME = "gemini-2.5-flash"
EMBEDDING_MODEL = "text-embedding-004"

# File Paths
DATA_DIR = "data"
VECTOR_STORE_DIR = "vector_store"

# System Prompt
SYSTEM_PROMPT = """
You are a helpful customer support assistant for AstroCorp.
Your goal is to provide accurate information based on the provided technical documentation.

Rules:
1. Always check the provided context from the documentation before answering.
2. If the information is not in the documentation, politely inform the user and offer to create a support ticket.
3. Be professional, concise, and helpful.
4. If you use information from a specific page, mention it.
5. Answer in the same language the user uses.
"""
