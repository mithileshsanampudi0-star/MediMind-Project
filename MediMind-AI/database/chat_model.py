from datetime import datetime

from database.mongo import MongoDB


class ChatModel:

    COLLECTION_NAME = "chat_history"

    @classmethod
    def collection(cls):
        return MongoDB.db()[cls.COLLECTION_NAME]

    @classmethod
    def save_message(
        cls,
        user_id,
        role,
        message
    ):

        document = {

            "user_id": str(user_id),

            "role": role,

            "message": message,

            "created_at": datetime.utcnow()

        }

        result = (
            cls.collection()
            .insert_one(document)
        )

        return str(
            result.inserted_id
        )

    @classmethod
    def get_chat_history(
        cls,
        user_id,
        limit=30
    ):

        messages = list(

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

        messages.reverse()

        return messages

    @classmethod
    def clear_chat_history(
        cls,
        user_id
    ):

        return cls.collection().delete_many(
            {
                "user_id":
                    str(user_id)
            }
        )