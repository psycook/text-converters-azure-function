# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(process_encoded_excel_blueprint) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints


import azure.functions as func
import logging
import pandas as pd
import io
import base64
import json

process_encoded_excel_blueprint = func.Blueprint()

@process_encoded_excel_blueprint.route(route="process_encoded_excel")
def process_encoded_excel(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Process encoded excel blueprint called')

    try:
        # Parse the request body to JSON
        req_body = req.get_json()

        # Extract and decode the base64 encoded Excel file
        base64_excel = req_body.get('document')
        if not base64_excel:
            return func.HttpResponse(
                "Please provide a base64 encoded Excel document.",
                status_code=400
            )
        excel_data = base64.b64decode(base64_excel)

        # Read Excel file into a pandas DataFrame
        excel_df = pd.read_excel(io.BytesIO(excel_data))

        # Convert the DataFrame to CSV
        output = io.StringIO()
        excel_df.to_csv(output, index=False)
        output.seek(0)
        csv_data = output.getvalue()

        # Encode the CSV data to base64
        base64_csv = base64.b64encode(csv_data.encode()).decode()

        # Prepare the JSON response
        response_json = json.dumps({"csv": csv_data})

        # Return the JSON response
        return func.HttpResponse(
            response_json,
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            f"An error occurred: {str(e)}",
            status_code=500
        )
