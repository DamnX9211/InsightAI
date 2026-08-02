from google import genai

from app.core.config import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


class AIService:

    @staticmethod
    def generate_summary(profile: dict) -> str:

        prompt = f"""
You are a senior data analyst.

Analyze the following dataset profile.

{profile}

Return:

1. Dataset quality summary

2. Biggest issues

3. Cleaning recommendations

4. Machine learning readiness

Keep it under 200 words.
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )

        return response.text