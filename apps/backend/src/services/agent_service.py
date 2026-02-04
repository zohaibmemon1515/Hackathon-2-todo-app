import os
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Agents SDK
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, RunConfig

# MCP
from mcp.server import call_mcp_tool

# ----------------------
# ENV & CONFIG
# ----------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("GITHUB_TOKEN") 

client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://models.inference.ai.azure.com"
)

model = OpenAIChatCompletionsModel(
    model="gpt-4o-mini",
    openai_client=client
)

# ----------------------
# PARAM SCHEMAS
# ----------------------
class AddTaskParams(BaseModel):
    title: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None
    reminder_at: Optional[str] = None

class UpdateTaskParams(BaseModel):
    task_id: int
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

# ----------------------
# TOOLS
# ----------------------
@function_tool
async def add_task(params: AddTaskParams, user_id: str):
    return await call_mcp_tool("add_task", user_id=user_id, **params.model_dump(exclude_none=True))

@function_tool
async def update_task(params: UpdateTaskParams, user_id: str):
    data = params.model_dump(exclude_none=True)
    task_id = data.pop("task_id")
    return await call_mcp_tool("update_task", user_id=user_id, task_id=task_id, **data)

@function_tool
async def list_tasks(params: ListTasksParams, user_id: str):
    result = await call_mcp_tool("list_tasks", user_id=user_id)
    if not result.get("success"): 
        return result
    
    tasks = result.get("tasks", [])
    if not tasks:
        return {"success": True, "response": "Aapki list abhi khali hai."}

    formatted = []
    for t in tasks:
        prio = f" [Prio: {t.get('priority')}]" if t.get('priority') else ""
        rem = f" [🔔 {t.get('reminder_at')}]" if t.get('reminder_at') else ""
        status = "✅" if t.get("is_completed") else "⏳"
        formatted.append(f"* {status} **{t.get('title')}** (ID: {t.get('id')}){prio}{rem}")
    
    return {"success": True, "response": "Aapki tasks:\n" + "\n".join(formatted)}

@function_tool
async def complete_task(params: TaskIdParams, user_id: str):
    return await call_mcp_tool("complete_task", user_id=user_id, task_id=params.task_id)

@function_tool
async def delete_task(params: TaskIdParams, user_id: str):
    return await call_mcp_tool("delete_task", user_id=user_id, task_id=params.task_id)

# ----------------------
# AGENT
# ----------------------
# ----------------------
# AGENT (Auto-Save Version)
# ----------------------
todo_agent = Agent(
    name="TodoAgent",
    model=model,
    instructions="""
Aap ek Task Architect hain. User ke tasks ko organize karna hai.

Workflow:
1. User se jo info mile, wahi use karein. Sirf missing details ko infer karein.
2. Task create karte hi, user ko ek **short summary** dikha dein:
   - 📌 Title
   - 🔥 Priority
   - ⏰ Reminder
   - 📝 Description / Tags
3. **Automatically save task** using add_task. 
4. Summary me inform karein ki task save ho gaya.
5. Mix language (Hinglish/Urdu) use karein.
"""
,
    tools=[add_task, update_task, list_tasks, complete_task, delete_task]
)


config = RunConfig(model=model, model_provider=client, tracing_disabled=True)

# ----------------------
# PROCESS REQUEST
# ----------------------
async def process_request(user_id: str, message: str, conversation_id: int, history_context: str = "") -> Dict[str, Any]:
    try:
        prompt = f"""
System Context:
user_id = {user_id}
Recent Conversation:
{history_context}

User Message:
{message}
"""
        result = await Runner.run(todo_agent, prompt, run_config=config)
        return {
            "success": True,
            "response": result.final_output,
            "conversation_id": conversation_id
        }
    except Exception as e:
        return {
            "success": False,
            "response": f"Masla agaya hai: {str(e)}",
            "conversation_id": conversation_id
        }
