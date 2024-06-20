Requirements:
Python 3.6 or higher
pandas
numpy
streamlit
easyocr
Pillow (PIL)
sqlite3
You can install the required packages using the following command:
pip install pandas numpy streamlit easyocr Pillow

Readme:
BizCardX: Extracting Business Card Data with OCR
Overview: BizCardX is a Python application designed to extract information from business cards. It utilizes various technologies such as Streamlit, Python, EasyOCR, PIL (Python Imaging Library), and SQLite3 database to achieve this functionality.

Functionality: The main purpose of BizCardX is to automate the process of extracting key details from business card images, such as the name, designation, company, contact information, email, website, address, and pincode. By leveraging the power of Optical Character Recognition (OCR) provided by EasyOCR, BizCardX is able to extract text from the images.

Technologies Used:

Python
Streamlit
EasyOCR
PIL (Python Imaging Library)
SQLite3
EasyOCR: EasyOCR is an open-source optical character recognition (OCR) library that enables developers to easily extract text from images. It uses deep learning techniques to accurately recognize text in images, making it a powerful tool for tasks such as document processing, image captioning, and text extraction from scanned documents.

Instructions:

Run the Streamlit application to interact with BizCardX.
The application allows you to upload a business card image, extract text from the image, and store the extracted data in a SQLite database.
You can view, modify, and delete business card data stored in the database.

Usage:

Open the Streamlit application.
Upload a business card image.
Extracted data will be displayed, allowing you to review and modify if needed.
Save the data to the SQLite database.
View, modify, or delete stored business card data based on your requirements.
Note: Ensure you have the necessary packages installed as mentioned in the requirements section before running the application.

Enjoy using BizCardX to streamline the process of extracting business card data efficiently!
