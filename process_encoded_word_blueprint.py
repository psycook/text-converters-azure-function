# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(process_encoded_word_blueprint) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints

import azure.functions as func
import logging
from docx import Document
import logging
import io
import base64
import json

process_encoded_word_blueprint = func.Blueprint()

@process_encoded_word_blueprint.route(route="process_encoded_word") 
def process_encoded_word(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Process encoded word document blueprint called')

    try:
        # Get the request body and decode the JSON
        req_body = req.get_json()

        # The base64 encoded data is assumed to be in a field named 'document'
        base64_data = req_body.get('document')
        if not base64_data:
            return func.HttpResponse(json.dumps({"error": "Please upload a Word document."}), 
                                     status_code=400, 
                                     mimetype="application/json")

        # Decode the base64 data
        decoded_data = base64.b64decode(base64_data)

        # Load the document using python-docx
        doc = Document(io.BytesIO(decoded_data))

        # Extract text from the document
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])

        # Return the result as JSON
        return func.HttpResponse(json.dumps({"text": text}), 
                                 mimetype="application/json")

    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), 
                                 status_code=500, 
                                 mimetype="application/json")
