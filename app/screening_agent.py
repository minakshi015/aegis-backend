from app.gemini_service import generate_response

SCREENING_PROMPT = """
You are a Mental Health Screening AI. Your goal is to assess the potential risk level of the user based on their input.
You are NOT a doctor and CANNOT diagnose.

Analysis Guidelines:
1. LOW RISK: General stress, fatigue, mild anxiety, normal life challenges.
2. MODERATE RISK: Persistent sadness, hopelessness, significant impact on daily function, withdrawal.
3. HIGH RISK / CRISIS: Mention of self-harm, suicide, severe trauma, immediate danger, hallucinations.

Format your response exactly as follows:
Risk Level: [LOW / MODERATE / HIGH]
Observation: [1-2 sentences explaining why, in supportive non-clinical language]
Guidance: [1 sentence suggestion, e.g., "Consider talking to a friend" or "Please call emergency services"]

Do not add any other text or disclaimers inside the formatted block (we handle disclaimers externally).
"""

def assess_risk(user_message: str) -> str:
    # 1. Check strict keywords locally first (Safety Net)
    msg_lower = user_message.lower()
    crisis_keywords = ["suicide", "kill myself", "die", "overdose", "hurt myself"]
    for word in crisis_keywords:
        if word in msg_lower:
            return "Risk Level: HIGH\nObservation: You shared feelings of immediate distress or self-harm.\nGuidance: Please contact emergency services or a crisis helpline immediately."

    # 2. Use Gemini for nuanced assessment
    prompt = f"{SCREENING_PROMPT}\n\nUser Input: {user_message}\nAssessment:"
    response = generate_response(prompt)
    
    if response.startswith("Error"):
        return "Risk Level: UNKNOWN\nObservation: Unable to process request.\nGuidance: Please try again or seek professional help if needed."
        
    return response
