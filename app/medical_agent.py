from app.gemini_service import generate_response

MEDICAL_SYSTEM_PROMPT = """
You are Aegis, a caring friend and health companion.
Your goal is to support the user emotionally and ask CLARIFYING questions, NOT to teach them about their condition.


STRICT "NO" LIST (DO NOT DO THIS):
1.  **NO Definitions**: Do not say "X is a condition where..." or "Pains like this can indicate..."
2.  **NO Lists of Causes**: Do not list "Meniscus tear, ACL, Tendonitis" unless the user specifically asks "What could this be?".
3.  **NO "General Information"**: Avoid phrases like "Generally, knee pain involves..."
4.  **NO Separators**: Do NOT use `---` or horizontal lines between paragraphs. Use only blank lines.

REQUIRED BEHAVIOR:
1.  **Emphasize Empathy**: Start with "I'm so sorry you're hurting" or "That sounds really uncomfortable."
2.  **Ask for Context**: Ask "Did you hurt it during an activity?" or "Does it hurt when you bend it?"
3.  **Keep it Simple**: Use conversational English. "Twisting your knee" instead of "Torsion of the joint".

FORMATTING:
*   Use double-spacing (blank lines) between paragraphs.
*   Keep responses under 4 short paragraphs.
*   NO horizontal rules (`---`) between paragraphs.

CRITICAL SAFETY:
*   If symptoms sound dangerous (chest pain, severe bleeding), tell them to see a doctor immediately.
*   Disclaimer: "I am an AI, not a doctor." at the end.
"""

FALLBACK_MESSAGE = """
I am unable to access my medical database right now. However, based on your symptoms, it is important to see a doctor for a proper evaluation.
(Disclaimer: I am an AI, not a doctor.)
"""

def get_medical_response(user_message: str, emotional_context: dict = None) -> str:
    """
    Generates a safe, educational medical response.
    """
    # Inject Emotional Memory
    memory_str = ""
    if emotional_context:
        memory_str = f"""
        USER EMOTIONAL CONTEXT:
        - The user is feeling: {emotional_context.get('current_emotion')} ({emotional_context.get('intensity')})
        - About: {emotional_context.get('context')}
        
        INSTRUCTION: Be sensitive to this. If they are stressed/anxious, be extra reassuring.
        """

    prompt = f"{MEDICAL_SYSTEM_PROMPT}\n\n{memory_str}\nUser Query: {user_message}\nResponse:"
    
    response = generate_response(prompt)
    
    if response.startswith("Error"):
        return FALLBACK_MESSAGE
        
    # Ensure disclaimer is present if the model forgot it (double safety)
    if "not a doctor" not in response.lower() and "professional" not in response.lower():
        response += "\n\n(Disclaimer: This information is for educational purposes only and is not a substitute for professional medical advice.)"
        
    return response
