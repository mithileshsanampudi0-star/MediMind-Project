class VoiceService:
    """
    Voice Processing Service

    Browser handles speech recognition using
    Web Speech API.

    Backend sanitizes and validates voice text.
    """

    def clean_transcript(
        self,
        transcript
    ):
        """
        Clean voice transcription.
        """

        if not transcript:
            return ""

        transcript = transcript.strip()

        transcript = transcript.replace(
            "\n",
            " "
        )

        transcript = transcript.replace(
            "\r",
            " "
        )

        transcript = " ".join(
            transcript.split()
        )

        return transcript

    def validate_symptoms(
        self,
        transcript
    ):
        """
        Validate voice symptom input.
        """

        cleaned = self.clean_transcript(
            transcript
        )

        if len(cleaned) < 3:
            return {
                "valid": False,
                "message": (
                    "Please provide more symptom details."
                )
            }

        return {
            "valid": True,
            "message": "Valid input",
            "text": cleaned
        }

    def symptoms_from_text(
        self,
        transcript
    ):
        """
        Convert speech text into symptom list.
        """

        cleaned = self.clean_transcript(
            transcript
        )

        separators = [
            ",",
            ";",
            " and "
        ]

        symptoms = [cleaned]

        for separator in separators:

            temp = []

            for item in symptoms:
                temp.extend(
                    item.split(separator)
                )

            symptoms = temp

        symptoms = [
            symptom.strip()
            for symptom in symptoms
            if symptom.strip()
        ]

        return symptoms


voice_service = VoiceService()