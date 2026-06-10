import os
from dotenv import load_dotenv
import ast

load_dotenv()

USER_NAME = os.getenv("USER_NAME")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

ASSISTANT_NAME = "ZORO"
AI_MODEL = "llama-3.3-70b-versatile" 