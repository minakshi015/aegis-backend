from app.gemini_service import generate_response
from app.wellness_agent import get_wellness_response

INTENT_PROMPT = """
Analyze the following user message and classify it into exactly one category: WELLNESS, MEDICAL, or CRISIS.

definitions:
- WELLNESS: General stress, motivation, sleep, routine, emotional support, lifestyle advice.
- MEDICAL: Specific physical symptoms (pain, rashes, infection), diagnoses, medication questions.
- CRISIS: Suicide, self-harm, severe trauma, immediate danger.

Respond ONLY with the category word.
"""

SAFETY_RESPONSE = """
I am an AI wellness guide, not a doctor. Since you mentioned medical symptoms or a potential health issue, I cannot provide advice.

Please consult a qualified healthcare professional for medical concerns.
"""

CRISIS_RESPONSE = """
It sounds like you are going through a difficult time. I am an AI and cannot provide the immediate help you might need.

If you are in danger or feeling suicidal, please contact emergency services immediately or call a helpline in your country (e.g., 988 in the US).
"""

# Simple keyword-based safety checklists (Backup)
CRISIS_KEYWORDS = ["suicide", "kill myself", "want to die", "self-harm", "hurt myself", "emergency"]
MEDICAL_KEYWORDS = ["pain", "chest", "heart", "stroke", "bleeding", "broken", "fever", "infection", "doctor", "symptom", "medical", "medicine", "pill", "rash", "lump", "headache", "nausea", "dizzy", "vomit", "injury"]

def classify_local(message: str) -> str:
    msg_lower = message.lower()
    if any(word in msg_lower for word in CRISIS_KEYWORDS): return "CRISIS"
    if any(word in msg_lower for word in MEDICAL_KEYWORDS): return "MEDICAL"
    return "WELLNESS"

def classify_intent(message: str) -> str:
    """
    Classifies intent using Gemini, with a fallback to local keywords if API fails (Rate Limit).
    """
    try:
        prompt = f"{INTENT_PROMPT}\n\nMessage: {message}\nCategory:"
        response = generate_response(prompt)
        
        if response.startswith("Error"):
             print(f"DEBUG: Intent API Limit hit, falling back to local. ({response})")
             return classify_local(message)

        clean_res = response.strip().upper()
        if "MEDICAL" in clean_res: return "MEDICAL"
        if "CRISIS" in clean_res: return "CRISIS"
        return "WELLNESS"
    except Exception as e:
        print(f"DEBUG: Intent Exception {e}, falling back to local.")
        return classify_local(message)

from app.medical_agent import get_medical_response

# --- EMOTIONAL MEMORY TRACKING ---
# In a real app, this would be a DB or Session Store.
# For now, we use a simple global dictionary for the single active user.
user_emotional_state = {
    "current_emotion": "Neutral",
    "intensity": "Low", 
    "context": "None"
}

def analyze_emotion(message: str):
    """
    Silent Agent: Extracts emotional context from the message to update state.
    """
    try:
        EMOTION_PROMPT = """
        Analyze the EMOTIONAL CONTENT of the user's message.
        Return ONLY a JSON string (no code blocks) with keys: 'emotion', 'intensity', 'context'.
        
        - emotion: one word (e.g., Anxiety, Sadness, Relief, Anger, Neutral)
        - intensity: Low, Medium, High
        - context: 2-3 words on the trigger (e.g., "Work Deadline", "Knee Pain", "Uncertainty")
        """
        prompt = f"{EMOTION_PROMPT}\n\nMessage: {message}\nJSON:"
        response = generate_response(prompt)
        
        # Simple cleanup to parse "fake" json if needed, or just string manipulation
        import json
        clean_res = response.replace('```json', '').replace('```', '').strip()
        data = json.loads(clean_res)
        
        # Update global state
        global user_emotional_state
        user_emotional_state["current_emotion"] = data.get("emotion", "Neutral")
        user_emotional_state["intensity"] = data.get("intensity", "Low")
        user_emotional_state["context"] = data.get("context", "None")
        
        print(f"DEBUG: MEMORY UPDATED -> {user_emotional_state}")
        
    except Exception as e:
        print(f"DEBUG: Memory update failed: {e}")

def route_request(message: str, history: list = []) -> tuple[str, str]:
    try:
        # 1. Update Emotional Memory (Silent)
        analyze_emotion(message)
        
        # 2. Classify Intent
        intent = classify_intent(message)
        print(f"DEBUG: ORCHESTRATOR DETECTED INTENT -> {intent}")

        # 2. Route
        if intent == "CRISIS":
            # Dynamic Crisis Response (New Persona) with Memory
            try:
                CRISIS_PROMPT = f"""
                You are Aegis, a Crisis Support AI.
                The user is expressing distress, self-harm, or suicidal thoughts.
                
                USER CONTEXT:
                - Emotional State: {user_emotional_state['current_emotion']}
                - Intensity: {user_emotional_state['intensity']}
                - Trigger: {user_emotional_state['context']}
                
                YOUR GOAL:
                1.  Respond with immediate empathy and validation.
                2.  Calmly encourage them to seek help.
                3.  Provide emergency resources (like 988).
                
                Tone: Compassionate, urgent but calm, non-judgmental.
                Format: Short paragraphs, double spacing.
                """
                prompt = f"{CRISIS_PROMPT}\n\nUser Message: {message}\nResponse:"
                response = generate_response(prompt)
                
                if not response or response.startswith("Error"):
                    return CRISIS_RESPONSE, "Crisis Guard"
                
                return response, "Crisis Guard"
            except Exception:
                return CRISIS_RESPONSE, "Crisis Guard"

        if intent == "MEDICAL":
            # Pass emotional context
            return get_medical_response(message, user_emotional_state), "Symptom Guidance Agent"
            
        # Default to Wellness Agent
        return get_wellness_response(message, history, user_emotional_state), "Wellness Agent"
    except Exception as e:
        return f"Error in orchestrator: {str(e)}", "System"
