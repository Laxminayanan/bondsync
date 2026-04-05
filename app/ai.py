import google.generativeai as genai
import os
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
    genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_relationship(memories, conflicts, weekly_checks):
    prompt = f"""
    Analyze the following couple relationship based on the user's data:
    Memories: {memories}
    Conflicts: {conflicts}
    Weekly Check-ins: {weekly_checks}

    Return a JSON block with exactly the following fields (DO NOT enclose in markdown formatting blocks):
    "bond_score": an integer from 0 to 10
    "emotional_compatibility": a string (e.g. "Excellent", "Good", "Needs Work")
    "communication_quality": a string description
    "conflict_health": a string description
    "advice": a string showing recommended advice
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        return {
            "bond_score": 8,
            "emotional_compatibility": "Good",
            "communication_quality": "Healthy and open",
            "conflict_health": "Occasional arguments, but resolves well.",
            "advice": "Keep communicating openly and planning nice activities together. (Add your Gemini API key in .env for real insights)"
        }
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]
        return json.loads(text)
    except Exception as e:
        return {
            "bond_score": 5,
            "emotional_compatibility": "Unknown",
            "communication_quality": "Generative AI error",
            "conflict_health": "Error processing",
            "advice": f"AI error occurred: {str(e)}"
        }
