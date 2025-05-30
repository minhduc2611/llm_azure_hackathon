import logging

# from azure.functions import HttpRequest, HttpResponse
import logging
import azure.functions as func
from multi_tool_agent.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.genai import types
from utils.cors import add_cors_headers

APP_NAME="ChatAgent"
USER_ID="user1234"
SESSION_ID="1234"

async def main(req: func.HttpRequest) -> func.HttpResponse:
    # Handle preflight OPTIONS request
    if req.method == "OPTIONS":
        return add_cors_headers(func.HttpResponse(status_code=200))

    try:
        query = req.params.get("query")
        if not query:
            return add_cors_headers(func.HttpResponse("Missing 'query' parameter", status_code=400))

        # Get session_id and user_id from the request (e.g., headers or query params)
        user_id = req.headers.get("X-User-ID", USER_ID)
        session_id = req.headers.get("X-Session-ID", SESSION_ID)

        # Initialize the persistent session service and runner if they are not global or
        # if the global instance needs to be re-initialized due to cold start.
        # For true persistence, these would ideally be initialized once at startup or
        # managed by a dependency injection framework.
        # However, for demonstration of getting rid of the error, we'll put them here.
        # In a real-world scenario with a persistent service, you'd likely initialize
        # session_service and runner globally *if* the service itself handles the persistence
        # and retrieval correctly across invocations.
        session_service = InMemorySessionService() # Placeholder - replace with persistent service
        memory_service = InMemoryMemoryService() # Use in-memory for demo

        # Check if session exists, otherwise create it (or let ADK handle it)
        logging.info(f">>>>>>>>>>>>>>> Getting session for user_id: {user_id}, session_id: {session_id}")
        res = await session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
        logging.info(f">>>>>>>>>>>>>>> Session: {res}")
        if res is None:
            logging.info(f">>>>>>>>>>>>>>> Creating session for user_id: {user_id}, session_id: {session_id}")
            await session_service.create_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
        user_input = types.Content(parts=[types.Part(text=query)], role="user")
        logging.info(f">>>>>>>>>>>>>>> New message: {user_input}")
        runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service, memory_service=memory_service)

        #  log the memory service
        logging.info(f">>>>>>>>>>>>>>> Memory service: {memory_service.search_memory(app_name=APP_NAME, user_id=user_id, query=query)}")
        # Interact with ADK agent
        events = runner.run(user_id=user_id, session_id=session_id, new_message=user_input)
        final_response = ""
        for event in events:
            if event.is_final_response():
                final_response = event.content.parts[0].text
                print("Agent Response: ", final_response)
        # Get the completed session
        completed_session1 = await runner.session_service.get_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)

        # Add this session's content to the Memory Service
        print("\n--- Adding Session 1 to Memory ---")
        memory_service = await memory_service.add_session_to_memory(completed_session1)
        print("Session added to memory.")
        
        return add_cors_headers(func.HttpResponse(final_response, status_code=200))

    except Exception as e:
        logging.error(f"Error: {e}")
        return add_cors_headers(func.HttpResponse(str(e), status_code=500))