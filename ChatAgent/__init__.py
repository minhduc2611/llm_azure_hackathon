import logging

# from azure.functions import HttpRequest, HttpResponse
import logging
import azure.functions as func
from multi_tool_agent.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

APP_NAME="ChatAgent"
USER_ID="user1234"
SESSION_ID="1234"

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        query = req.params.get("query")
        if not query:
            return func.HttpResponse("Missing 'query' parameter", status_code=400)

        # Get session_id and user_id from the request (e.g., headers or query params)
        user_id = req.headers.get("X-User-ID", "default_user")
        session_id = req.headers.get("X-Session-ID", "default_session")

        # Initialize the persistent session service and runner if they are not global or
        # if the global instance needs to be re-initialized due to cold start.
        # For true persistence, these would ideally be initialized once at startup or
        # managed by a dependency injection framework.
        # However, for demonstration of getting rid of the error, we'll put them here.
        # In a real-world scenario with a persistent service, you'd likely initialize
        # session_service and runner globally *if* the service itself handles the persistence
        # and retrieval correctly across invocations.
        session_service = InMemorySessionService() # Placeholder - replace with persistent service
        # Check if session exists, otherwise create it (or let ADK handle it)
        try:
            session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
        except ValueError: # Session not found, create it
            session_service.create_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)

        runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

        # Interact with ADK agent
        events = runner.run(user_id=user_id, session_id=session_id, new_message=query)
        final_response = ""
        for event in events:
            if event.is_final_response():
                final_response = event.content.parts[0].text
                print("Agent Response: ", final_response)
        return func.HttpResponse(final_response, status_code=200)

    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(str(e), status_code=500)