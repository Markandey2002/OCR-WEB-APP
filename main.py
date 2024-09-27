import os
import urllib.request
import platform
import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import cv2
import numpy as np
import re
import shutil

# Function to install Tesseract based on the OS
def install_tesseract():
    if platform.system() == "Linux":
        # Install Tesseract for Linux
        if not shutil.which('tesseract'):
            os.system("sudo apt-get update")
            os.system("sudo apt-get install -y tesseract-ocr")
    elif platform.system() == "Windows":
        # Install Tesseract for Windows
        tesseract_url = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20201127.exe"
        tesseract_exe_path = "tesseract-installer.exe"
        if not shutil.which('tesseract'):
            urllib.request.urlretrieve(tesseract_url, tesseract_exe_path)
            os.system(tesseract_exe_path)
            os.remove(tesseract_exe_path)
        
        # Set the Tesseract path for Windows
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    else:
        st.error("Unsupported OS: Tesseract installation not available.")
        return

# Ensure Tesseract is installed and configured
install_tesseract()

# Function to extract text from an image
def extract_text(image):
    try:
        img = Image.open(image)

        # Preprocess the image for better OCR accuracy
        img = img.convert('L')  # Convert to grayscale
        img = img.filter(ImageFilter.SHARPEN)  # Sharpen image
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)  # Enhance contrast

        # Extract text using Tesseract for both Hindi and English
        extracted_text = pytesseract.image_to_string(img, lang='hin+eng', config='--psm 6')

        return extracted_text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

# Function for advanced preprocessing using OpenCV (optional)
def preprocess_image(image):
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
    gray = cv2.GaussianBlur(gray, (5, 5), 0)  # Reduce noise with Gaussian Blur
    _, threshold_img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)  # Thresholding
    return Image.fromarray(threshold_img)

# Function to highlight a keyword in the extracted text
def highlight_keyword(text, keyword):
    highlighted_text = re.sub(f'({re.escape(keyword)})', r'<mark>\1</mark>', text, flags=re.IGNORECASE)
    return highlighted_text

# Main Streamlit application
def main():
    st.title("OCR Web Application")
    st.write("Upload an image containing text in Hindi and English for OCR processing.")

    # File uploader for image
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

        # Extract text from the image
        with st.spinner("Extracting text from image..."):
            extracted_text = extract_text(uploaded_file)

        # Display the extracted text
        st.text_area("Extracted Text", extracted_text, height=300)

        # Keyword search functionality
        search_keyword = st.text_input("Enter keyword to search in extracted text:")
        if search_keyword:
            # Check if the keyword exists in the extracted text
            if search_keyword.lower() in extracted_text.lower():
                st.success(f"Keyword found: '{search_keyword}'")

                # Highlight the keyword in the extracted text
                highlighted_text = highlight_keyword(extracted_text, search_keyword)

                # Display the highlighted text using st.markdown to render HTML
                st.markdown(highlighted_text, unsafe_allow_html=True)
            else:
                st.error(f"Keyword '{search_keyword}' not found.")
                # Show original text if keyword is not found
                st.text_area("Extracted Text", extracted_text, height=300)

if __name__ == '__main__':
    main()
