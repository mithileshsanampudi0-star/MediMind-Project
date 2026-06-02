from pypdf import PdfReader


class PDFExtractionService:
    """
    PDF Text Extraction Service (pypdf version)

    - Lightweight
    - No native compilation issues
    - Works well on ARM64 systems
    """

    def extract_text(self, pdf_path):
        """
        Extract full text from PDF file.
        """

        try:
            reader = PdfReader(pdf_path)

            extracted_text = []

            for page in reader.pages:

                text = page.extract_text()

                if text:
                    extracted_text.append(text)

            return "\n".join(extracted_text)

        except Exception as error:

            raise RuntimeError(
                f"PDF extraction failed: {error}"
            )

    def extract_preview(self, pdf_path, max_characters=1500):
        """
        Extract limited preview text.
        """

        text = self.extract_text(pdf_path)

        return text[:max_characters]

    def validate_pdf_content(self, pdf_path):
        """
        Validate whether PDF contains readable text.
        """

        try:

            text = self.extract_text(pdf_path)

            if not text or not text.strip():

                return {
                    "valid": False,
                    "message": "No readable text found in PDF."
                }

            return {
                "valid": True,
                "message": "PDF content extracted successfully."
            }

        except Exception as error:

            return {
                "valid": False,
                "message": str(error)
            }


pdf_extraction_service = PDFExtractionService()