import logging

from azure.functions import HttpRequest, HttpResponse
import logging
import azure.functions as func
from multi_tool_agent.agent import root_agent

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        query = req.params.get("query")
        if not query:
            return func.HttpResponse("Missing 'query' parameter", status_code=400)

        # Interact with ADK agent
        result = root_agent.invoke(query)

        return func.HttpResponse(result, status_code=200)

    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(str(e), status_code=500)
