from database.analysis_model import AnalysisModel


class HistoryService:
    """
    Handles analysis history operations.
    """

    @staticmethod
    def get_user_history(
        user_id,
        limit=50
    ):

        try:

            history = (
                AnalysisModel.get_user_history(
                    user_id=user_id,
                    limit=limit
                )
            )

            return history

        except Exception as error:

            print(
                f"History Service Error: {error}"
            )

            return []

    @staticmethod
    def get_history_summary(
        user_id
    ):

        try:

            total_analyses = (
                AnalysisModel.total_analyses(
                    user_id
                )
            )

            emergency_cases = (
                AnalysisModel.emergency_cases(
                    user_id
                )
            )

            return {
                "total_analyses":
                    total_analyses,

                "emergency_cases":
                    emergency_cases
            }

        except Exception:

            return {
                "total_analyses": 0,
                "emergency_cases": 0
            }