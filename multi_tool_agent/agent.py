from google.adk.agents import LlmAgent
from google.adk.tools import Tool, ToolCall, ToolCallResult

# --- TOOL DEFINITION ---
class SearchManualsTool(Tool):
    name = "search_manuals"
    description = "Search manuals and provide step-by-step instructions."

    def call(self, tool_call: ToolCall) -> ToolCallResult:
        query = tool_call.input.get("query", "")
        return ToolCallResult(
            output={
                "result": f"Steps for '{query}': 1. Read the manual. 2. Follow instructions. 3. Done!"
            }
        )

# --- AGENT SETUP ---
root_agent = LlmAgent(
    name="instruction_bot",
    model="gpt-4o-mini",  # Replace with model available to you
    description="An assistant that helps users get step-by-step instructions.",
    instructions=(
        "You are a helpful assistant. Provide concise, accurate manuals or steps to complete tasks. "
        "If needed, use the 'search_manuals' tool."
    ),
    tools=[SearchManualsTool()],
)
