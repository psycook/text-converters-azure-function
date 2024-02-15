# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(process_word_blueprint) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints

import azure.functions as func
import logging
import io
from docx import Document

process_word_blueprint = func.Blueprint()

@process_word_blueprint.route(route="process_word") 
def process_word(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Process word document blueprint called')

    for name, value in req.headers.items():
        logging.info(f"Header: {name} = {value}")
    
    if req.files:
        for filename, file in req.files.items():
            # Log file details
            logging.info(f"File received: {filename}")
            logging.info(f"File type: {file.content_type}")
            logging.info(f"File size: {len(file.read())} bytes")

            # Important: Go back to the beginning of the file if you plan to read it again
            file.seek(0)
    else:
        logging.info("No files found in the request.")
    try:
        # Read the file from the request
        file = req.files.get('document')

        if not file:
            return func.HttpResponse("Please upload a Word document.", status_code=400)

        # Load the document using python-docx
        doc = Document(io.BytesIO(file.read()))

        # Extract text from the document
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])

        return func.HttpResponse(text, mimetype="text/plain")

    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
    