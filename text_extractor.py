import PyPDF2

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.

    Parameters:
        pdf_path (str): The path of the PDF file to extract text from.
    Returns:
        str: The extracted text from the PDF file.
    Raises:
        Exception: If an error occurs during the extraction process.
    """
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            pdf_text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_text += page.extract_text()
            return pdf_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    pdf_path = "path/to/your/pdf/file.pdf"
    extracted_text = extract_text_from_pdf(pdf_path)
    if extracted_text:
        print("Extracted Text:")
        print(extracted_text)
    else:
        print("Failed to extract text from the PDF.")
