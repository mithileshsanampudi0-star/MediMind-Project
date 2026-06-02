from database.mongo import MongoDB
from config import Config


class MapsService:
    """
    Hospital Search Service
    Uses MongoDB-backed hospital database
    """

    def __init__(self):
        self.db = MongoDB.get_database()
        self.hospitals_db = self.db["hospitals_directory"]

    def geocode_location(self, location):
        """
        Simulate geocoding with location lookup.
        """
        
        # For demo: return approximate coords for major cities
        city_coords = {
            "london": {"latitude": 51.5074, "longitude": -0.1278},
            "new york": {"latitude": 40.7128, "longitude": -74.0060},
            "paris": {"latitude": 48.8566, "longitude": 2.3522},
            "tokyo": {"latitude": 35.6762, "longitude": 139.6503},
            "sydney": {"latitude": -33.8688, "longitude": 151.2093},
            "mumbai": {"latitude": 19.0760, "longitude": 72.8777},
            "delhi": {"latitude": 28.7041, "longitude": 77.1025},
            "bangalore": {"latitude": 12.9716, "longitude": 77.5946},
        }

        location_lower = location.lower().strip()

        if location_lower in city_coords:
            coords = city_coords[location_lower]
            return {
                "latitude": coords["latitude"],
                "longitude": coords["longitude"],
                "formatted_address": location
            }

        # Default fallback
        return {
            "latitude": 20.5937,
            "longitude": 78.9629,
            "formatted_address": location
        }

    def search_nearby_hospitals(
        self,
        latitude,
        longitude,
        radius=None
    ):
        """
        Search hospitals from MongoDB database.
        """

        try:
            hospitals = list(
                self.hospitals_db.find(
                    {},
                    {"_id": 0}
                ).limit(Config.MAX_HOSPITAL_RESULTS)
            )

            return hospitals

        except Exception as error:
            raise RuntimeError(
                f"Hospital search failed: {str(error)}"
            )

    def get_nearby_hospitals(
        self,
        location_text
    ):
        """
        Location text -> Hospital Search
        """

        coordinates = self.geocode_location(
            location_text
        )

        if not coordinates:
            return []

        return self.search_nearby_hospitals(
            coordinates["latitude"],
            coordinates["longitude"]
        )

    def seed_hospitals(self):
        """
        Populate hospital database with demo data.
        """

        try:
            # Check if already seeded
            if self.hospitals_db.count_documents({}) > 0:
                return

            demo_hospitals = [
                {
                    "name": "City General Hospital",
                    "address": "123 Main Street, London",
                    "rating": "4.5",
                    "phone": "+44 20 7946 0958",
                    "specialty": "General Medicine",
                    "location": {"lat": 51.5074, "lng": -0.1278},
                    "maps_url": "https://www.openstreetmap.org/?mlat=51.5074&mlon=-0.1278&zoom=16"
                },
                {
                    "name": "Royal Medical Center",
                    "address": "456 King Road, London",
                    "rating": "4.7",
                    "phone": "+44 20 7946 0959",
                    "specialty": "Cardiology",
                    "location": {"lat": 51.5080, "lng": -0.1270},
                    "maps_url": "https://www.openstreetmap.org/?mlat=51.5080&mlon=-0.1270&zoom=16"
                },
                {
                    "name": "St. Mary's Hospital",
                    "address": "789 Oxford Street, London",
                    "rating": "4.6",
                    "phone": "+44 20 7946 0960",
                    "specialty": "Pediatrics",
                    "location": {"lat": 51.5100, "lng": -0.1240},
                    "maps_url": "https://www.openstreetmap.org/?mlat=51.5100&mlon=-0.1240&zoom=16"
                },
                {
                    "name": "Mount Sinai Medical Center",
                    "address": "100 Madison Avenue, New York",
                    "rating": "4.8",
                    "phone": "+1 212-241-6500",
                    "specialty": "Oncology",
                    "location": {"lat": 40.7850, "lng": -73.9760},
                    "maps_url": "https://www.openstreetmap.org/?mlat=40.7850&mlon=-73.9760&zoom=16"
                },
                {
                    "name": "Hôpital de la Pitié-Salpêtrière",
                    "address": "47 Boulevard de l'Hôpital, Paris",
                    "rating": "4.5",
                    "phone": "+33 1 42 17 80 00",
                    "specialty": "Neurology",
                    "location": {"lat": 48.8398, "lng": 2.3633},
                    "maps_url": "https://www.openstreetmap.org/?mlat=48.8398&mlon=2.3633&zoom=16"
                }
            ]

            self.hospitals_db.insert_many(demo_hospitals)

        except Exception:
            pass


class LazyMapsService:
    """Lazy-loading wrapper for MapsService to avoid MongoDB connection at import time."""
    
    def __init__(self):
        self._service = None
    
    def _get_service(self):
        if self._service is None:
            self._service = MapsService()
        return self._service
    
    def seed_hospitals(self):
        return self._get_service().seed_hospitals()
    
    def geocode_location(self, location):
        return self._get_service().geocode_location(location)
    
    def search_nearby_hospitals(self, latitude, longitude, radius=None):
        return self._get_service().search_nearby_hospitals(latitude, longitude, radius)
    
    def get_nearby_hospitals(self, location_text):
        return self._get_service().get_nearby_hospitals(location_text)


maps_service = LazyMapsService()
