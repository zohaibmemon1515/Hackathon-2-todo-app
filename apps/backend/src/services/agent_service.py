import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from pydantic import BaseModel

# agents SDK
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    function_tool,
    RunConfig
)

# MCP
from ..mcp.server import call_mcp_tool

# --------------------------------------------------
# ENV
# --------------------------------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("GEMINI_API_KEY")
# --------------------------------------------------
# Tool Parameter Schemas
# --------------------------------------------------

class AddTaskParams(BaseModel):
    title: str
    description: Optional[str] = None

class CompleteTaskParams(BaseModel):
    task_id: int

class DeleteTaskParams(BaseModel):
    task_id: int

class UpdateTaskParams(BaseModel):
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

class ListTasksParams(BaseModel):
    pass 

# --------------------------------------------------
# TOOLS (⚠️ @function_tool IS REQUIRED)
# --------------------------------------------------

@function_tool
async def add_task(params: AddTaskParams, user_id: str):
    """Add a new task"""
    return await call_mcp_tool(
        "add_task",
        user_id=user_id,  # UUID string
        title=params.title,
        description=params.description,
    )

@function_tool
async def complete_task(params: CompleteTaskParams, user_id: str):
    """Complete a task"""
    return await call_mcp_tool(
        "complete_task",
        user_id=user_id,
        task_id=params.task_id,  # integer
    )

@function_tool
async def delete_task(params: DeleteTaskParams, user_id: str):
    """Delete a task"""
    return await call_mcp_tool(
        "delete_task",
        user_id=user_id,
        task_id=params.task_id,  # integer
    )

@function_tool
async def update_task(params: UpdateTaskParams, user_id: str):
    """Update an existing task"""
    data = params.model_dump(exclude_none=True)
    task_id = data.pop("task_id")
    return await call_mcp_tool(
        "update_task",
        user_id=user_id,
        task_id=task_id,  # integer
        **data,
    )

@function_tool
async def list_tasks(params: ListTasksParams, user_id: str):
    """List all tasks for the user with integer IDs"""
    result = await call_mcp_tool(
        "list_tasks",
        user_id=user_id,  # UUID string
    )

    if not result.get("success"):
        return result

    tasks = result.get("tasks", [])
    formatted_tasks = []
    for task in tasks:
        formatted_tasks.append({
            "task_id": task.get("id"),  # integer ID
            "title": task.get("title", ""),
            "description": task.get("description", ""),
            "is_completed": task.get("is_completed", False)
        })

    # Update the tasks in the result
    result["tasks"] = formatted_tasks

    # Agent-friendly summary
    if formatted_tasks:
        result["response"] = "Here is your task list:\n" + "\n".join(
            [f"* **{t['title']}** (ID: {t['task_id']}) - {'Completed' if t['is_completed'] else 'Not completed'}" for t in formatted_tasks]
        )
    else:
        result["response"] = "You don't have any tasks on your list right now. Would you like to add a new task?"

    return result

# --------------------------------------------------
# MODEL + CLIENT (Gemini via OpenAI SDK)
# --------------------------------------------------

external_client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# --------------------------------------------------
# AGENT
# --------------------------------------------------

todo_agent = Agent(
    name="TodoAgent",
    model=model,
    instructions="""
You are a helpful AI assistant that manages a user's todo list.

You can:
- add tasks
- complete tasks
- update tasks
- delete tasks
- list tasks

Rules:
- Always confirm the action taken
- Be short and friendly
- Use tools whenever an action is required
- When listing tasks, include task_id (integer) for each task
The user_id is provided in the system context (UUID string).
""",
    tools=[
        add_task,
        complete_task,
        delete_task,
        update_task,
        list_tasks,
    ],
)

# --------------------------------------------------
# MAIN PROCESS FUNCTION
# --------------------------------------------------

async def process_request(
    user_id: str,          # UUID string
    message: str,
    conversation_id: int,
) -> Dict[str, Any]:

    try:
        prompt = f"""
System Context:
user_id = {user_id}

User Message:
{message}
"""

        result = await Runner.run(todo_agent, prompt, run_config=config)

        return {
            "success": True,
            "response": result.final_output,
            "metadata": {
                "tool_calls": getattr(result, "tool_calls", []),
            },
            "conversation_id": conversation_id,
        }

    except Exception as e:
        print("Agent Error:", str(e))

        return {
            "success": False,
            "response": "Sorry, something went wrong while processing your request.",
            "metadata": {},
            "conversation_id": conversation_id,
        }
