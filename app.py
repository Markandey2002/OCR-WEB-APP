import os
import streamlit as st
from PIL import Image
from ocr_preprocess import preprocess_image, enhance_image
from ocr_engine import install_tesseract, extract_text
import re
import pytesseract

# Set the Tesseract path (modify if necessary)
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if not os.path.exists(tesseract_path):
    st.error("Tesseract is not installed or the path is incorrect. Please check your installation.")
else:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

# Ensure Tesseract is installed and configured
install_tesseract()

# Function to highlight a keyword in the extracted text
def highlight_keyword(text, keyword):
    highlighted_text = re.sub(f'({re.escape(keyword)})', r'<mark>\1</mark>', text, flags=re.IGNORECASE)
    return highlighted_text

# Main Streamlit application
def main():
    st.title("OCR Web Application (Hindi + English)")
    st.write("Upload an image for OCR processing.")

    # File uploader for image
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

        # Preprocess the image for better OCR accuracy
        with st.spinner("Processing image..."):
            image = Image.open(uploaded_file)
            processed_image = preprocess_image(image)
            enhanced_image = enhance_image(processed_image)

        # Extract text from the preprocessed and enhanced image
        with st.spinner("Extracting text..."):
            extracted_text = extract_text(enhanced_image)

        # Display the extracted text
        st.text_area("Extracted Text", extracted_text, height=300)

        # Keyword search functionality
        search_keyword = st.text_input("Enter keyword to search in extracted text:")
        if search_keyword:
            if search_keyword.lower() in extracted_text.lower():
                st.success(f"Keyword found: '{search_keyword}'")
                highlighted_text = highlight_keyword(extracted_text, search_keyword)
                st.markdown(highlighted_text, unsafe_allow_html=True)
            else:
                st.error(f"Keyword '{search_keyword}' not found.")
                st.text_area("Extracted Text", extracted_text, height=300)

if __name__ == '__main__':
    main()
