import streamlit as st
import text_extractor
import os
import shutil

st.title("summarizED - PDF Summarizer")

target_directory = './pdfs'
shutil.copy(source_file, target_directory)


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Get the file path
    # file_path = os.path.join("pdfs", filename)  # Save the file in the 'uploads' folder

    filename = uploaded_file.name
    file_extension = os.path.splitext(file_name)[1]


# filename = input("Enter filename: ")
# filepath = f"./pdfs/{filename}.pdf"
extracted_text = text_extractor.extract_text_from_pdf(file_path)
print(f"Extracted Text: {extracted_text}")

st.write(extracted_text)