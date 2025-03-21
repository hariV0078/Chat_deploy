from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from google import genai  # Corrected import
from groq import Groq
from pydantic import BaseModel
from typing import Optional
import os
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app setup
app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API keys
GOOGLE_API_KEY = "AIzaSyB9_uEfeyLvJ1O-PrT8Qlj8PlOG-p_MvsU"
GROQ_API_KEY = "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"

# Initialize API Clients
client = genai.Client(api_key=GOOGLE_API_KEY)  # Proper initialization
groq_client = Groq(api_key=GROQ_API_KEY)

# Define system prompt properly
SYSTEM_PROMPT = """
You are EcoGuide, an AI assistant dedicated to promoting cleanliness, proper waste management, and eco-friendly habits. Your goal is to educate users, solve waste-related challenges, and inspire sustainable actions.

Tone:
- Friendly, encouraging, and non-judgmental
- Use simple language and avoid jargon
- Add light emojis (🌱♻️🗑️) to emphasize key points

Key Topics:
1. Waste disposal guidelines (recycling, composting, hazardous waste)
2. Local garbage collection schedules
3. Reducing plastic use and reusable alternatives
4. Troubleshooting common issues
5. Community initiatives and educational content

Rules:
- Do not provide medical/legal advice
- Redirect to official sources when unsure
- Acknowledge cultural differences
- Encourage actionable steps
"""

class ChatbotRequest(BaseModel):
    user_query: str
    user_info: Optional[str] = None

@app.post("/chatbot")
async def chatbot(request: ChatbotRequest):
    try:
        #  # Use correct model name
        
        # Structure the prompt correctly
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser Query: {request.user_query}\nAdditional Info: {request.user_info or ''}"
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",contents=[full_prompt]
        )
        
        return JSONResponse(content={"response": response.text})
    except Exception as e:
        logger.error(f"Error in chatbot response: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
