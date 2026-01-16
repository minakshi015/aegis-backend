
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database import supabase

# Initialize FastAPI app
# Initialize FastAPI app
app = FastAPI(
    title="Minimal Backend Skeleton",
    description="A lightweight FastAPI backend skeleton.",
    version="0.1.0"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConversationInput(BaseModel):
    message: str

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns:
        dict: {"status": "ok"}
    """
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Mental Health Agent API is running", "docs": "/docs"}

from fastapi.responses import JSONResponse
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return JSONResponse(content={})

@app.post("/conversations")
async def create_conversation(input_data: ConversationInput):
    """
    Create a new conversation record.
    """
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase client not initialized")
    
    try:
        response = supabase.table("conversations").insert({"message": input_data.message}).execute()
        return response.data[0] if response.data else {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversations")
async def get_conversations():
    """
    Retrieve recent conversations.
    """
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase client not initialized")
    
    try:
        response = supabase.table("conversations").select("*").order("created_at", desc=True).limit(10).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from app.gemini_service import generate_response

class LLMRequest(BaseModel):
    prompt: str

@app.post("/llm/test")
async def test_llm(request: LLMRequest):
    """
    Test Gemini API integration.
    """
    response_text = generate_response(request.prompt)
    if response_text.startswith("Error"):
        raise HTTPException(status_code=500, detail=response_text)
    return {"response": response_text}

from app.wellness_agent import get_wellness_response

@app.post("/chat/wellness")
async def chat_wellness(input_data: ConversationInput):
    """
    Get wellness guidance from the AI agent with memory.
    """
    # 1. Fetch recent history (Last 5 messages)
    history = []
    if supabase:
        try:
            # Fetch last 5 conversations
            result = supabase.table("conversations").select("*").order("created_at", desc=True).limit(5).execute()
            if result.data:
                # Reverse to chronological order
                for row in reversed(result.data):
                    history.append({"role": "user", "content": row['message']})
                    if row['response']:
                        history.append({"role": "assistant", "content": row['response']})
                print(f"DEBUG: Fetched {len(history)/2} pairs of history for prompt context.")
        except Exception as e:
            print(f"Error fetching history: {e}")

    # 2. Generate Response
    print(f"DEBUG: Generating response with history: {history}")
    response = get_wellness_response(input_data.message, history)
    
    if response.startswith("Error"):
         raise HTTPException(status_code=500, detail=response)

    # 3. Save Interaction to Supabase
    if supabase:
        try:
            # We strip the disclaimer for storage if we want clean history, but here we store as served
            # Or better, store it. The prompt formatter will see it in history.
            supabase.table("conversations").insert({
                "message": input_data.message, 
                "response": response
            }).execute()
        except Exception as e:
            print(f"Error saving conversation: {e}")
            
    return {"response": response}

from app.orchestrator import route_request

@app.post("/chat")
async def chat_orchestrated(input_data: ConversationInput):
    """
    Unified chat endpoint with intent orchestration.
    """
    # 1. Fetch recent history (Reuse logic)
    history = []
    if supabase:
        try:
            result = supabase.table("conversations").select("*").order("created_at", desc=True).limit(5).execute()
            if result.data:
                for row in reversed(result.data):
                    history.append({"role": "user", "content": row['message']})
                    if row['response']:
                        history.append({"role": "assistant", "content": row['response']})
        except Exception as e:
            print(f"Error fetching history: {e}")

    # 2. Route Request via Orchestrator
    response_text, agent_name = route_request(input_data.message, history)
    
    if response_text.startswith("Error"):
         # Instead of crashing (500), return a friendly message
         print(f"DEBUG: API Error: {response_text}")
         response_text = "I'm currently experiencing high traffic. Please wait a moment and try again."

    # 3. Save Interaction
    if supabase:
        try:
            supabase.table("conversations").insert({
                "message": input_data.message, 
                "response": response_text
                # Note: We aren't saving 'agent_name' to DB yet in the basic schema, but we pass it to UI
            }).execute()
        except Exception as e:
            print(f"Error saving conversation: {e}")
            
    return {"response": response_text, "agent": agent_name}

from app.screening_agent import assess_risk

@app.post("/chat/screening")
async def chat_screening(input_data: ConversationInput):
    """
    Screening endpoint to assess risk level.
    """
    assessment = assess_risk(input_data.message)
    assessment = assess_risk(input_data.message)
    return {"response": assessment}

from app.medical_agent import get_medical_response

@app.post("/chat/medical")
async def chat_medical(input_data: ConversationInput):
    """
    Medical symptom checker endpoint.
    """
    response = get_medical_response(input_data.message)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
