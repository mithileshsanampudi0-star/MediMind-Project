import os

from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from config import Config


class GroqService:
    """
    Central Groq LLM Service
    """

    def __init__(self):
        os.environ["GROQ_API_KEY"] = Config.GROQ_API_KEY

        self.llm = ChatGroq(
            model=Config.GROQ_MODEL,
            temperature=Config.GROQ_TEMPERATURE,
            max_tokens=Config.GROQ_MAX_TOKENS
        )

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response from a raw text prompt.
        Matches the required interface for direct LLM calls.
        """
        try:
            response = self.llm.invoke(prompt)
            
            if hasattr(response, "content"):
                return response.content
            
            return str(response)
            
        except Exception as error:
            raise RuntimeError(
                f"Groq direct generation failed: {str(error)}"
            )

    def generate(
        self,
        prompt_template: str,
        variables: dict
    ):
        """
        Execute template-based prompt and return response.
        """
        try:
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=list(variables.keys())
            )

            chain = prompt | self.llm

            response = chain.invoke(variables)

            if hasattr(response, "content"):
                return response.content

            return str(response)

        except Exception as error:
            raise RuntimeError(
                f"Groq generation failed: {str(error)}"
            )

    def health_check(self):
        """
        Validate Groq connectivity.
        """
        try:
            response = self.llm.invoke("Reply with: OK")

            if hasattr(response, "content"):
                return response.content

            return "OK"

        except Exception as error:
            return f"Connection Failed: {str(error)}"


# Global instance
groq_service = GroqService()