import text_extractor

filename = input("Enter filename: ")
filepath = f"./pdfs/{filename}.pdf"
print(f"Extracted Text: {text_extractor.extract_text_from_pdf(filepath)[:100]}")

