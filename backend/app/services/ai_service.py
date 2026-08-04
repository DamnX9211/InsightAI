from typing import Any

from google import genai
import json

from websockets import Data

from app.core.config import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


class AIService:

    @staticmethod

    def build_ai_payload(
        dataset: dict[str, Any],
        profile: dict[str, Any],
        health: dict[str, Any],
    ) -> dict[str, Any]:

        return {
            "dataset": {
                "rows": dataset["rows"],
                "columns": dataset["columns"],
                "numeric_columns": dataset["numeric_columns"],
                "categorical_columns": dataset["categorical_columns"],
            },
            "health": {
                "score": health["score"],
                "issues": health["issues"],
            },
            "quality": {
                "missing_values": profile["missing_values"],
                "missing_percentage": profile["missing_percentage"],
                "duplicate_rows": profile["duplicate_rows"],
            },
            "column_types": profile["column_types"],
        }


    @staticmethod
    def generate_summary(profile: dict) -> str:


        prompt = f"""
You are a senior Data Quality Engineer.

The dataset has already been profiled.

The health score has already been calculated.

Do NOT invent new statistics.
Do NOT change the health score.
Base every statement only on the supplied data.

Dataset Profile:
{json.dumps(profile, indent=2)}

Return ONLY valid JSON in this exact format:

{{
  "overall_quality": "<use the existing health score to describe quality>",
  "ml_readiness": "<High | Medium | Low>",
  "critical_issues": [
    "...",
    "..."
  ],
  "recommendations": [
    "...",
    "..."
  ]
}}

Rules:

- Do not use markdown.
- Do not wrap the response in code fences.
- Never invent columns or statistics.
- Maximum 4 issues.
- Maximum 5 recommendations.
- Keep every recommendation under one sentence.
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        return json.loads(text)