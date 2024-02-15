# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(process_excel_blueprint) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints
import azure.functions as func
import logging
import pandas as pd
import io

process_excel_blueprint = func.Blueprint()

@process_excel_blueprint.route(route="process_excel")
def process_excel(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Process Excel blueprint called')

    try:
        file = req.files.get('document')
        if not file:
            return func.HttpResponse("Please upload an Excel file.", status_code=400)

        # Ensure the stream is at the beginning
        file.stream.seek(0)

        # Read Excel file into a pandas DataFrame
        excel_data = pd.read_excel(file.stream)

        # Convert the DataFrame to CSV
        output = io.StringIO()
        excel_data.to_csv(output, index=False)
        output.seek(0)

        return func.HttpResponse(output.getvalue(), mimetype="text/csv", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)
