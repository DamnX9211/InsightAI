from pydantic import BaseModel


class AISummary(BaseModel):
    overall_quality: str
    ml_readiness: str

    critical_issues: list[str]
    recommendations: list[str]