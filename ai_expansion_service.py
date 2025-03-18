from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import anthropic
import logging
import threading
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger('ai_expansion_service')

# Initialize FastAPI app
app = FastAPI(title="Shrthnder AI Expansion Service")

# Initialize the Anthropics client with API key from environment
api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key:
    logger.warning("ANTHROPIC_API_KEY not found in environment variables. AI expansion will not work.")
else:
    logger.info("ANTHROPIC_API_KEY found. AI expansion is ready to use.")

client = anthropic.Anthropic(api_key=api_key)

class ExpandRequest(BaseModel):
    context: str  # e.g., "legal", "medical", etc.
    query: str    # abbreviated text

@app.post("/expand")
async def expand_abbreviation(request: ExpandRequest):
    # Define a system prompt that instructs the model to expand abbreviated text based on context.
    system_prompt = (
        "You are a language expansion assistant. Your task is to expand abbreviated text into its full form. "
        "You will be provided with a context and an abbreviated sentence. Consider the context and fill in missing vowels, letters, "
        "and words to form a clear, complete sentence."
    )

    # Build the user message which includes both the context and the abbreviated text.
    user_text = (
        f"Context: {request.context}\n"
        f"Abbreviated text: {request.query}\n"
        f"Expanded text:"
    )

    try:
        # Call the Anthropics API using the provided client.messages.create() syntax.
        message = client.messages.create(
            model="claude-3-7-sonnet-20250219",  # You may change the model if needed.
            max_tokens=1000,
            temperature=1,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_text
                        }
                    ]
                }
            ]
        )
        # Return the expanded text from the API response.
        logger.info(f"Expanded text: {message.content}")
        return {"expanded_text": message.content.strip()}
    except Exception as e:
        logger.error(f"Error expanding text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Function to start the API server
def start_api_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

# Function to start the API server in a separate thread
def start_api_server_thread():
    thread = threading.Thread(target=start_api_server, daemon=True)
    thread.start()
    logger.info("API server started on http://127.0.0.1:8000")
    return thread 