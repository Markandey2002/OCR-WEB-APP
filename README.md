OCR Web Application (Hindi + English)
A simple web application to extract text from images using Tesseract OCR. Supports both Hindi and English text extraction.

Featu![Screenshot 2024-09-28 152750](https://github.com/user-attachments/assets/1bf91d5b-ef58-4ccb-866f-9ae50fe36630)
![Screenshot 2024-09-28 152810](https://github.com/user-attachments/assets/0ba81ae8-2eb0-4f9b-825d-fc847f254e05)
res![Screenshot 2024-09-28 152825](https://github.com/user-attachments/assets/dbe6180f-f2d4-43ce-88f8-1b9e243aa855)

Upload images in .jpg, .jpeg, or .png formats.
Extract text from images using Tesseract.
Search for keywords in the extracted text.
How to Run Locally
Prerequisites
Python 3.x
Tesseract OCR (Download from here and add to PATH).
Steps
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/ocr-web-app.git
cd ocr-web-app
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the app:

bash
Copy code
streamlit run app.py
Open your browser and visit:

arduino
Copy code
http://localhost:8501
Deployment
Ensure requirements.txt and packages.txt are properly configured.
Deploy on Streamlit Cloud by connecting your GitHub repository.
