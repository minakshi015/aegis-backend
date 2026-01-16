from app.gemini_service import generate_response

SYSTEM_PROMPT = """
You are Aegis, a warm and supportive wellness guide.
Your goal is to help the user feel heard and grounded.

FORMATTING RULES:
*   **Double Spacing**: ALWAYS leave a blank line between paragraphs.
*   **Short Blocks**: No paragraph should be longer than 2 sentences.
*   **Bullet Points**: Use them for suggestions to make it easy to read.
*   **NO Separators**: Do NOT use `---` or horizontal rules between paragraphs.


Structure your response as follows:
1.  **Empathize**: Acknowledge their feeling warmly.
2.  **Suggest**: Offer 1-2 simple, actionable things (breathing, water, rest).
3.  **Check-in**: Ask how they are feeling about that.

Tone: Gentle, human, unhurried, and calm.
"""

def get_wellness_response(user_message: str, history: list = [], emotional_context: dict = None) -> str:
    """
    Generates a wellness-focused response using Gemini, wrapped with system instructions.
    Args:
        user_message: The current message from the user.
        history: List of dicts [{'role': 'user'|'assistant', 'content': '...'}]
        emotional_context: Dict with 'current_emotion', 'intensity', 'context'
    """
    # Format history into a conversation block
    context_str = ""
    if history:
        context_str = "PREVIOUS CONTEXT (History of this conversation):\n"
        for msg in history:
            role = "User" if msg['role'] == 'user' else "Assistant"
            context_str += f"{role}: {msg['content']}\n"
        context_str += "---\n"

    # Inject Emotional Memory
    memory_str = ""
    if emotional_context:
        memory_str = f"""
        EMOTIONAL MEMORY:
        - User is feeling: {emotional_context.get('current_emotion')}
        - Intensity: {emotional_context.get('intensity')}
        - Context/Trigger: {emotional_context.get('context')}
        
        INSTRUCTION: Acknowledge this emotion gently if relevant.
        """

    # Simple prompt concatenation for the basic Gemini API usage
    full_prompt = f"{SYSTEM_PROMPT}\n\n{memory_str}\n{context_str}CURRENT MESSAGE:\nUser: {user_message}\nAssistant:"
    
    response = generate_response(full_prompt)
    
    # Append disclaimer if the response was generated successfully
    if response and not response.startswith("Error"):
        # Ensure distinct separation
        disclaimer = "This support is meant for reflection and grounding only and is not a substitute for professional mental health care."
        
        # Check if the LLM already generated the disclaimer (common if it sees it in history)
        if disclaimer not in response:
            return response + "\n\n---\n" + disclaimer
        else:
            return response
        
    return response
