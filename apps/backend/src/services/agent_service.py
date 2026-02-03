import os
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
from pydantic import BaseModel, Field

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
# ENV & CONFIG
# --------------------------------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash", 
    openai_client=external_client,
)

# --------------------------------------------------
# Tool Parameter Schemas
# --------------------------------------------------

class AddTaskParams(BaseModel):
    title: str = Field(description="Task ka main title (Required).")
    description: Optional[str] = Field(default=None, description="Task details (Optional).")
    tags: Optional[List[str]] = Field(default=None, description="Keywords jaise ['work', 'personal'] (Optional).")
    priority: Optional[str] = Field(default=None, description="High, Medium, ya Low (Optional).")
    due_date: Optional[str] = Field(default=None, description="Deadline date (Optional).")
    reminder_at: Optional[str] = Field(default=None, description="Reminder time (Optional).")

class UpdateTaskParams(BaseModel):
    task_id: int = Field(description="Jis task ko update karna hai uski ID.")
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None
    reminder_at: Optional[str] = None

class TaskIdParams(BaseModel):
    task_id: int

class ListTasksParams(BaseModel):
    pass

# --------------------------------------------------
# TOOLS
# --------------------------------------------------

@function_tool
async def add_task(params: AddTaskParams, user_id: str):
    """Naya task save karne ke liye. Sirf tab chalayein jab user confirm karde."""
    return await call_mcp_tool("add_task", user_id=user_id, **params.model_dump(exclude_none=True))

@function_tool
async def update_task(params: UpdateTaskParams, user_id: str):
    """Purane task ki details badalne ke liye."""
    data = params.model_dump(exclude_none=True)
    task_id = data.pop("task_id")
    return await call_mcp_tool("update_task", user_id=user_id, task_id=task_id, **data)

@function_tool
async def list_tasks(params: ListTasksParams, user_id: str):
    """User ke saare tasks list karne ke liye."""
    result = await call_mcp_tool("list_tasks", user_id=user_id)
    if not result.get("success"): return result
    
    tasks = result.get("tasks", [])
    if not tasks:
        return {"success": True, "response": "Aapki list abhi khali hai."}

    formatted = []
    for t in tasks:
        prio = f" [Prio: {t.get('priority')}]" if t.get('priority') else ""
        rem = f" [🔔 {t.get('reminder_at')}]" if t.get('reminder_at') else ""
        status = "✅" if t.get("is_completed") else "⏳"
        formatted.append(f"* {status} **{t.get('title')}** (ID: {t.get('id')}){prio}{rem}")
    
    return {"success": True, "response": "Aapki tasks ye rahi:\n" + "\n".join(formatted)}

@function_tool
async def complete_task(params: TaskIdParams, user_id: str):
    """Task ko completed mark karne ke liye."""
    return await call_mcp_tool("complete_task", user_id=user_id, task_id=params.task_id)

@function_tool
async def delete_task(params: TaskIdParams, user_id: str):
    """Task delete karne ke liye."""
    return await call_mcp_tool("delete_task", user_id=user_id, task_id=params.task_id)

# --------------------------------------------------
# AGENT DEFINITION
# --------------------------------------------------

todo_agent = Agent(
    name="TodoAgent",
    model=model,
    instructions="""
Aap ek Advanced Task Architect hain. Aapka kaam user se details le kar structured tasks banana hai.

### Rules:
1. **The Interview**: Agar user kahe "Add task", toh pehle Title poochein. Title milne par baaki fields (Description, Priority, Reminder, Tags, Due Date) ke baare mein poochein aur batayein ke ye optional hain.
2. **Context**: Agar user message mein time (e.g. 5pm) ya priority (e.g. Urgent) bataye, toh usay store karein aur dobara na poochein.
3. **Confirmation**: Tool (`add_task`) chalane se pehle user ko summary dikhayein:
   "Theek hai! Main ye task bana raha hoon:
   📌 Title: [Title]
   ⏰ Reminder: [Time]
   🔥 Priority: [High/Low]
   Kya main isay save kar doon?"
4. **Execution**: Jab user "yes" ya "save it" kahe, tabhi `add_task` call karein.
""",
    tools=[add_task, update_task, list_tasks, complete_task, delete_task],
)

config = RunConfig(model=model, model_provider=external_client, tracing_disabled=True)

# --------------------------------------------------
# MAIN PROCESS FUNCTION
# --------------------------------------------------

# --------------------------------------------------
# MAIN PROCESS FUNCTION (FIXED)
# --------------------------------------------------

async def process_request(
    user_id: str, 
    message: str, 
    conversation_id: int, 
    history_context: str = "" # Pichli baatein string format mein
) -> Dict[str, Any]:
    try:
        # Pichli history ko prompt ka hissa banayein taaki 'Runner' ko context mile
        full_prompt = f"""
System Context:
user_id = {user_id}
Recent Conversation History:
{history_context}

User Message:
{message}
"""
        # Runner.run() ab bina kisi 'history' argument ke chalega
        result = await Runner.run(todo_agent, full_prompt, run_config=config)

        return {
            "success": True,
            "response": result.final_output,
            "conversation_id": conversation_id,
            # Nayi history update karke bhejien (Example format)
            "updated_history": f"{history_context}\nUser: {message}\nAgent: {result.final_output}"
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            "success": False, 
            "response": f"Masla agaya hai: {str(e)}", 
            "conversation_id": conversation_id
        }