from typing import Dict


class HealthScoreAgent:
    """
    Generates a health score from
    risk level and emergency status.
    """

    @staticmethod
    def calculate_score(
        risk_level: str,
        emergency: bool = False
    ) -> Dict:

        risk = (
            risk_level or ""
        ).lower()

        score = 100

        if risk == "low":
            score = 90

        elif risk == "medium":
            score = 65

        elif risk == "high":
            score = 35

        if emergency:
            score -= 20

        score = max(0, score)

        if score >= 80:
            status = "Excellent"

        elif score >= 60:
            status = "Moderate"

        elif score >= 40:
            status = "Needs Attention"

        else:
            status = "Critical"

        return {
            "health_score": score,
            "health_status": status
        }