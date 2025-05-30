from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

# --- TOOL DEFINITION ---
def search_manuals(query: str) -> dict:    
    return {"status": "success", "report": f"Steps for '{query}': 1. Read the manual. 2. Follow instructions. 3. Done!"}

search_manuals_tool = FunctionTool(func=search_manuals)

# --- AGENT SETUP ---
root_agent = LlmAgent(
    name="instruction_bot",
    model="gpt-4o-mini",  # Replace with model available to you
    description="An assistant that helps users get step-by-step instructions.",
    tools=[search_manuals_tool],
    instruction=(
        "You are a helpful assistant. Provide concise, accurate manuals or steps to complete tasks. If needed, use the 'search_manuals' tool."
    ),
)
