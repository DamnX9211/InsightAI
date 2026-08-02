from typing import Any

class HealthScoreService:

    @staticmethod
    def calculate_health_score(profile: dict[str, Any]) -> dict:

        score = 100
        issues = []

        # missing values
        for column, percentage in profile["missing_percentage"].items():
            if percentage > 20:
                score -= 20
                issues.append(
                    f"Column '{column}' has {percentage}% missing values."
                )

            elif percentage > 5:
                score -= 10
                issues.append(
                    f"Column '{column}' has {percentage}% missing values."
                )

        # duplicate rows
        duplicate = profile["duplicate_rows"]

        if duplicate > 0:
            score -= 10
            issues.append(
                f"{duplicate} duplicate rows detected."
            )            

        score = max(score, 0)

        return {
            "score": score,
            "issues": issues,
        }    