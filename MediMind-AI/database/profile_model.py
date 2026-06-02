from datetime import datetime

from database.mongo import MongoDB


class ProfileModel:

    COLLECTION_NAME = "profiles"

    @classmethod
    def collection(cls):
        return MongoDB.db()[cls.COLLECTION_NAME]

    @classmethod
    def save_profile(
        cls,
        user_id,
        age,
        gender,
        blood_group,
        allergies,
        conditions
    ):

        profile = {

            "user_id": str(user_id),

            "age": age,

            "gender": gender,

            "blood_group": blood_group,

            "allergies": allergies,

            "conditions": conditions,

            "updated_at": datetime.utcnow()

        }

        cls.collection().update_one(

            {
                "user_id": str(user_id)
            },

            {
                "$set": profile
            },

            upsert=True

        )

        return True

    @classmethod
    def get_profile(
        cls,
        user_id
    ):

        return cls.collection().find_one(
            {
                "user_id": str(user_id)
            }
        )

    @classmethod
    def delete_profile(
        cls,
        user_id
    ):

        return cls.collection().delete_one(
            {
                "user_id": str(user_id)
            }
        )