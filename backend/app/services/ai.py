import google.generativeai as genai
import os

# Initialize Gemini model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def ask_gemini(prompt: str) -> str:
    """Get AI response from Gemini."""
    response = model.generate_content(prompt)
    return response.text
