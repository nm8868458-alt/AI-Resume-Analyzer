import os
import json
from dotenv import load_dotenv

load_dotenv()

HAS_GEMINI = False

try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    pass


def analyze_resume_with_gemini(resume_text):
    """
    Analyze resume using Gemini AI
    """

    # If Gemini package not installed
    if not HAS_GEMINI:
        return {
            "score": 50,
            "summary": "Gemini package not installed.",
            "skills": ["Python"],
            "missing": ["Docker"],
            "recommendations": [
                "Install Gemini package correctly."
            ]
        }

    # Read API key from Render Environment Variable
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        return {
            "score": 0,
            "summary": "GOOGLE_API_KEY not found in environment variables.",
            "skills": ["N/A"],
            "missing": ["N/A"],
            "recommendations": [
                "Add GOOGLE_API_KEY in Render Environment Variables."
            ]
        }

    try:
        # Configure Gemini
        genai.configure(api_key=api_key)

        # Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
        You are an ATS Resume Analyzer.

        Analyze this resume and return ONLY valid JSON.

        Resume:
        {resume_text}

        Format:
        {{
            "score": 85,
            "summary": "Short summary",
            "skills": ["skill1", "skill2"],
            "missing": ["missing1", "missing2"],
            "recommendations": ["tip1", "tip2"]
        }}
        """

        response = model.generate_content(prompt)

        content = response.text.strip()

        # Remove markdown formatting if exists
        content = content.replace("```json", "")
        content = content.replace("```", "")

        data = json.loads(content)

        return data

    except Exception as e:
        print("Gemini Error:", e)

        return {
            "score": 50,
            "summary": "Could not perform deep analysis.",
            "skills": ["Python"],
            "missing": ["Docker"],
            "recommendations": [
                "Check API key",
                "Try again later"
            ]
        }
