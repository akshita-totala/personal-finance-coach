import pdfplumber


def extract_text_from_pdf(pdf_path):
    """
    Reads a PDF and returns all text as a single string.
    """

    text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    except FileNotFoundError:
        raise Exception("PDF file not found.")

    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")