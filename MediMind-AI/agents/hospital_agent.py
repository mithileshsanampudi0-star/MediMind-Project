from database.mongo import MongoDB
from services.maps_service import maps_service
from utils.helpers import current_timestamp


class HospitalAgent:
    """
    Hospital Recommendation Agent

    Responsibilities:
    - Find nearby hospitals
    - Rank hospitals
    - Store search history
    - Provide specialist-aware recommendations
    """

    def recommend(
        self,
        location,
        specialist=None
    ):
        """
        Search hospitals near patient location.
        """

        try:

            hospitals = maps_service.get_nearby_hospitals(
                location
            )

            if hospitals:

                self._store_search(
                    location,
                    specialist,
                    hospitals
                )

            return {
                "success": True,
                "hospitals": hospitals
            }

        except Exception as error:

            return {
                "success": False,
                "hospitals": [],
                "error": str(error)
            }

    def top_hospitals(
        self,
        location,
        specialist=None,
        limit=5
    ):
        """
        Return highest-rated hospitals.
        """

        result = self.recommend(
            location,
            specialist
        )

        if not result["success"]:
            return result

        hospitals = result["hospitals"]

        hospitals = sorted(
            hospitals,
            key=lambda x: (
                float(x["rating"])
                if str(x["rating"]).replace(
                    ".",
                    ""
                ).isdigit()
                else 0
            ),
            reverse=True
        )

        return {
            "success": True,
            "hospitals": hospitals[:limit]
        }

    def _store_search(
        self,
        location,
        specialist,
        hospitals
    ):
        """
        Store hospital search history.
        """

        try:

            MongoDB.hospitals_collection().insert_one(
                {
                    "location": location,
                    "specialist": specialist,
                    "results_count": len(hospitals),
                    "hospitals": hospitals,
                    "searched_at": current_timestamp()
                }
            )

        except Exception:
            pass

    def recent_searches(
        self,
        limit=10
    ):
        """
        Fetch recent hospital searches.
        """

        try:

            searches = list(
                MongoDB.hospitals_collection()
                .find()
                .sort(
                    "searched_at",
                    -1
                )
                .limit(limit)
            )

            return searches

        except Exception:
            return []


hospital_agent = HospitalAgent()