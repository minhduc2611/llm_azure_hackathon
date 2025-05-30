from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.adk.models.lite_llm import LiteLlm

# --- TOOL DEFINITION ---
def search_kone_elevator_manuals_to_fix_buttons(query: str) -> dict:
    """
    Searches KONE elevator manuals to find steps and instructions for fixing issues related to elevator buttons.
    Use this tool when a user asks for help with KONE elevator buttons or needs a manual to troubleshoot them.

    Args:
        query: The specific problem or question about KONE elevator buttons for which the user needs a manual or fix.
    """
    return {"status": "success", "report": f"Steps for '{query}': 1. Preparations & Safety 2. Access the Button Assembly . 3. Inspect Wiring & Harness  4. Remove & Test the Individual Button Module 5. Clean or Replace the Faulty Switch 6. Reassemble the Button Module"}

search_kone_elevator_manuals_to_fix_buttons_tool = FunctionTool(func=search_kone_elevator_manuals_to_fix_buttons)

# --- AGENT SETUP ---
root_agent = LlmAgent(
    name="instruction_bot",
    model=LiteLlm(model="openai/o4-mini"),
    description="An assistant that helps users get step-by-step instructions.",
    tools=[search_kone_elevator_manuals_to_fix_buttons_tool],
    instruction=(
        "You are a helpful assistant. Provide concise, accurate manuals or steps to complete tasks.\n"
        "**ALWAYS** use the `search_kone_elevator_manuals_to_fix_buttons` tool when the user asks for "
        "help with KONE elevator buttons, needs to fix KONE elevator buttons, or requires a manual related to KONE elevator button repair or troubleshooting. "
        "If the user's query is about general instructions or tasks not specific to KONE elevator buttons, try to answer directly if possible."
        "Return exact steps from the manual. Do not make up your own steps. Dont add more details than the manual provides."
    ),
)
