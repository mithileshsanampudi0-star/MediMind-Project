from datetime import datetime

from database.mongo import MongoDB


class AnalysisModel:

    COLLECTION_NAME = "analyses"

    @classmethod
    def collection(cls):
        return MongoDB.db()[cls.COLLECTION_NAME]

    @classmethod
    def save_analysis(

        cls,

        user_id,

        symptoms,

        diseases,

        risk_level,

        specialist,

        emergency,

        health_score,

        analysis_text

    ):

        document = {

            "user_id":
                str(user_id),

            "symptoms":
                symptoms,

            "predicted_diseases":
                diseases,

            "risk_level":
                risk_level,

            "specialist":
                specialist,

            "emergency":
                emergency,

            "health_score":
                health_score,

            "analysis":
                analysis_text,

            "created_at":
                datetime.utcnow()

        }

        result = (

            cls.collection()
            .insert_one(document)

        )

        return str(
            result.inserted_id
        )

    @classmethod
    def get_user_history(
        cls,
        user_id,
        limit=100
    ):

        return list(

            cls.collection()

            .find(
                {
                    "user_id":
                        str(user_id)
                }
            )

            .sort(
                "created_at",
                -1
            )

            .limit(limit)

        )

    @classmethod
    def get_latest_analysis(
        cls,
        user_id
    ):

        return cls.collection().find_one(

            {
                "user_id":
                    str(user_id)
            },

            sort=[
                (
                    "created_at",
                    -1
                )
            ]

        )

    @classmethod
    def total_analyses(
        cls,
        user_id=None
    ):

        query = {}

        if user_id:

            query["user_id"] = (
                str(user_id)
            )

        return (
            cls.collection()
            .count_documents(query)
        )

    @classmethod
    def emergency_cases(
        cls,
        user_id=None
    ):

        query = {
            "emergency": True
        }

        if user_id:

            query["user_id"] = (
                str(user_id)
            )

        return (
            cls.collection()
            .count_documents(query)
        )

    @classmethod
    def average_health_score(
        cls,
        user_id=None
    ):

        query = {}

        if user_id:

            query["user_id"] = (
                str(user_id)
            )

        analyses = list(
            cls.collection().find(query)
        )

        if not analyses:
            return 0

        total = sum(

            analysis.get(
                "health_score",
                0
            )

            for analysis in analyses

        )

        return round(
            total / len(analyses),
            2
        )