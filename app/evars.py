import os
from dotenv import load_dotenv


load_dotenv()

# Flask settings
DEBUG = bool(os.getenv("DEBUG", True))
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5005))

# AI settings
AI_CHAT_MODEL_PROVIDER = os.getenv("AI_CHAT_MODEL_PROVIDER")
AI_EMBEDDING_MODEL_PROVIDER = os.getenv("AI_EMBEDDING_MODEL_PROVIDER")

AI_CHAT_MODEL_NAME = os.getenv("AI_CHAT_MODEL_NAME")
AI_EMBEDDING_MODEL_NAME = os.getenv("AI_EMBEDDING_MODEL_NAME")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Web Scraper
WEBSCRAPER_TYPE = os.getenv("WEBSCRAPER_TYPE", "DEFAULT")
HTTP_TIMEOUT = int(os.getenv("HTTP_TIMEOUT", 15))
GOOGLE_SEARCH_PROVIDER = os.getenv("GOOGLE_SEARCH_PROVIDER", "GOOGLESEARCHPKG")

# Text chunk size
AI_TEXT_CHUNK_TOKEN_SIZE = int(os.getenv("AI_TEXT_CHUNK_TOKEN_SIZE", 800))
AI_TEXT_CHUNK_OVERLAP_TOKEN_SIZE = int(os.getenv("AI_TEXT_CHUNK_OVERLAP_SIZE", -1))

# In-Memory IndexDB
INDEXDB_TYPE = os.getenv("INDEXDB_TYPE", "HNSW")
