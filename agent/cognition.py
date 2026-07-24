import os
import json
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_student(problem, confidence):

    # Determine confidence and cognitive load in Python
    if confidence <= 3:
        confidence_level = "Very Low"
        cognitive_load = "High"

    elif confidence <= 6:
        confidence_level = "Moderate"
        cognitive_load = "Medium"

    else:
        confidence_level = "High"
        cognitive_load = "Low"

    prompt = f"""
You are NeuroBridge's AI Cognition Agent.

Analyze the student's learning behaviour.

Student Problem:
{problem}

Student Confidence:
{confidence}/10

Confidence Level:
{confidence_level}

Estimated Cognitive Load:
{cognitive_load}

Return ONLY valid JSON in the following format:

{{
    "problem_type":"",
    "confidence_level":"{confidence_level}",
    "cognitive_load":"{cognitive_load}",
    "emotion":"",
    "learning_style":"",
    "recommended_strategy":"",
    "next_step":""
}}

Choose:

- problem_type
- emotion
- learning_style
- recommended_strategy
- next_step

Return ONLY JSON.

Do NOT use markdown.
Do NOT use triple backticks.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        text = response.text.strip()

        # Remove markdown if Gemini returns it
        if text.startswith("```"):
            text = (
                text.replace("```json", "")
                .replace("```", "")
                .strip()
            )

        return json.loads(text)

    except Exception as e:

        return {
            "error": str(e)
        }