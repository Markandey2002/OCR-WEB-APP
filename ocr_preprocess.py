import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

# Function to preprocess image using OpenCV for better OCR accuracy
def preprocess_image(image):
    # Ensure the image is valid
    if image is None:
        raise ValueError("Input image is None")

    img = np.array(image)

    # Handle different image formats
    if img.ndim == 2:  # Grayscale image
        gray = img
    elif img.shape[2] == 3:  # RGB image
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
    elif img.shape[2] == 4:  # RGBA image
        # Convert RGBA to RGB, then to Grayscale
        img_rgb = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    else:
        raise ValueError("Invalid image format: Expected 1 or 3 or 4 channels, got {}".format(img.shape))

    # Apply Gaussian blur
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply binary thresholding
    _, threshold_img = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Additional morphology to reduce noise
    kernel = np.ones((1, 1), np.uint8)
    processed_img = cv2.morphologyEx(threshold_img, cv2.MORPH_CLOSE, kernel)

    return Image.fromarray(processed_img)

# Function to enhance the image
def enhance_image(image):
    img = image.convert('L')  # Convert to grayscale
    img = img.filter(ImageFilter.SHARPEN)  # Sharpen image
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)  # Enhance contrast

    return img
