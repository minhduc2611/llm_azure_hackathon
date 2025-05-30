import logging
import azure.functions as func
import os
import openai
from dotenv import load_dotenv
from utils.summary import gen_summary
# Load .env
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info("Starting the function")
        query = req.params.get("query")
        if not query:
            return func.HttpResponse("Missing 'query' parameter", status_code=400)
        logging.info(f"Query: {query}")
        
        summary = gen_summary(query)

        return func.HttpResponse(summary)

    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(e, status_code=500)
