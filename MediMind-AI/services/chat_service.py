from services.groq_service import groq_service
from database.chat_model import ChatModel


class ChatService:

    @staticmethod
    def medical_chat(
        user_id,
        user_message
    ):

        try:

            ChatModel.save_message(
                user_id=user_id,
                role="user",
                message=user_message
            )

            prompt = f"""
You are MediMind AI.

You are a healthcare pre-diagnosis assistant.

Rules:
- Do not provide final medical diagnoses.
- Ask follow-up questions when needed.
- Provide health guidance.
- Recommend emergency care if symptoms are dangerous.
- Keep answers concise and professional.

Patient Message:
{user_message}
"""

            ai_response = groq_service.generate_response(
                prompt
            )

            ChatModel.save_message(
                user_id=user_id,
                role="assistant",
                message=ai_response
            )

            return ai_response

        except Exception as error:

            print(
                f"Chat Service Error: {error}"
            )

            return (
                "Unable to generate response "
                "at the moment."
            )

    @staticmethod
    def get_chat_history(
        user_id
    ):

        try:

            return (
                ChatModel.get_chat_history(
                    user_id
                )
            )

        except Exception:

            return []

    @staticmethod
    def clear_chat(
        user_id
    ):

        try:

            ChatModel.clear_chat_history(
                user_id
            )

            return True

        except Exception:

            return False