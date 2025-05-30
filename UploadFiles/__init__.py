import logging
import azure.functions as func
from utils.file import upload_file_to_blob, get_signed_url
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        files = req.files.getlist('files')  # <--- This only works with multipart/form-data
        id_value = req.form.get('id')
        logging.info(f"====================================req.files: {req.files} ===========================")
        if not files:
            return func.HttpResponse("No files uploaded", status_code=400)

        uploaded_urls_json = []
        for file in files:
            filename = file.filename
            logging.info(f"Uploading file: {filename}")
            blob_path, blob_url = upload_file_to_blob(file.stream, filename, id_value)
            logging.info(f"Uploaded: {blob_url}")
            signed_url, expiry_minutes, expiry_date = get_signed_url(blob_path)
            uploaded_urls_json.append({"blob_path": blob_path, "blob_url": signed_url, "expiry_minutes": expiry_minutes, "expiry_date": expiry_date})
        json_response = json.dumps({"uploaded_urls": uploaded_urls_json})
        return func.HttpResponse(json_response, status_code=200)

    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(str(e), status_code=500)
