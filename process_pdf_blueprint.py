# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(process_pdf_blueprint) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints


import azure.functions as func
import logging
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

process_pdf_blueprint = func.Blueprint()

@process_pdf_blueprint.route(route="process_pdf")
def process_pdf(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Process pdf called.')

    try:
        # Read the PDF from the request
        pdf_file = req.files['pdf'].read()  # Read as bytes

        # Extract text from the PDF
        extracted_text = extract_text_from_pdf(pdf_file)

        # Return the extracted text
        return func.HttpResponse(extracted_text, status_code=200)
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(f"Error occurred: {str(e)}", status_code=500)

def extract_text_from_pdf(pdf_bytes):
    # Open the PDF from bytes
    doc = fitz.open(stream=pdf_bytes, filetype='pdf')
    full_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Extract text from page
        text = page.get_text()
        full_text += text + "\n"

        # Extract images from page
        for img_index, img in enumerate(page.get_images()):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            # Open the image with PIL and perform OCR
            image = Image.open(io.BytesIO(image_bytes))
            image_text = pytesseract.image_to_string(image)
            full_text += image_text + "\n"
    
    doc.close()
    return full_text