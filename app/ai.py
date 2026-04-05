from google import genai
import os
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def analyze_relationship(memories, conflicts, weekly_checks):
    prompt = f"""
    Analyze the following couple relationship based on the user's data:
    Memories: {memories}
    Conflicts: {conflicts}
    Weekly Check-ins: {weekly_checks}

    Return ONLY a JSON object:
    {{
        "bond_score": number (0–10),
        "emotional_compatibility": string,
        "communication_quality": string,
        "conflict_health": string,
        "advice": string
    }}
    """

    if not GEMINI_API_KEY:
        return {
            "bond_score": 8,
            "emotional_compatibility": "Good",
            "communication_quality": "Healthy",
            "conflict_health": "Balanced",
            "advice": "Add GEMINI_API_KEY for real AI insights"
        }

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        return json.loads(text)

    except Exception as e:
        return {
            "bond_score": 5,
            "emotional_compatibility": "Unknown",
            "communication_quality": "AI error",
            "conflict_health": "Error",
            "advice": f"AI error occurred: {str(e)}"
        }
