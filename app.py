import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Configure Gemini
genai.configure(api_key=api_key)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# Create FastAPI app
app = FastAPI(
    title="JARVIS AI Backend",
    description="A simple AI assistant backend powered by Gemini",
    version="1.0.0"
)

# Enable CORS so frontend can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Later restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class ChatRequest(BaseModel):
    message: str

# Health check route
@app.get("/")
def root():
    return {
        "status": "online",
        "message": "JARVIS backend is running successfully!"
    }

# Chat route
@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = model.generate_content(request.message)

        return {
            "success": True,
            "reply": response.text
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
