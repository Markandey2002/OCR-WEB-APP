import pytesseract
from PIL import Image
import platform
import os
import urllib.request
import shutil
from ocr_preprocess import preprocess_image  # Importing preprocess_image

# Function to install and configure Tesseract based on the OS
def install_tesseract():
    if platform.system() == "Linux":
        if not shutil.which('tesseract'):
            os.system("sudo apt-get update")
            os.system("sudo apt-get install -y tesseract-ocr")
    elif platform.system() == "Windows":
        tesseract_url = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20201127.exe"
        tesseract_exe_path = "tesseract-installer.exe"
        if not shutil.which('tesseract'):
            urllib.request.urlretrieve(tesseract_url, tesseract_exe_path)
            os.system(tesseract_exe_path)
            os.remove(tesseract_exe_path)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    else:
        raise OSError("Unsupported OS: Tesseract installation not available.")

# Function to extract text using improved Tesseract config
def extract_text(image):
    try:
        # Convert image to grayscale, enhance contrast and sharpness
        img = preprocess_image(image)  # Ensure preprocess_image is defined and imported
        
        # Extract Hindi and English text using Tesseract
        extracted_text = pytesseract.image_to_string(img, lang='hin+eng', config='--psm 6')
        
        return extracted_text
    except Exception as e:
        return f"Error extracting text: {str(e)}"
