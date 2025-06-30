from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
import uvicorn
from agents.master_router import supervisor, pretty_print_messages
import time
from agents.memory import get_memory_agent
from agents.master_router import llm

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    # Optionally, add session_id here if you want to support per-user sessions
    # session_id: str

@app.post("/query")
def query_endpoint(request: QueryRequest):
    st = time.time()
    session_id = "default-session" 
    memory_agent, memory = get_memory_agent(llm=llm, session_id=session_id)
    for chunk in supervisor.stream({
        "messages": [
            {"role": "user", "content": request.query}
        ]
    }):
        pretty_print_messages(chunk)
    final_message_history = chunk["supervisor"]["messages"]
    print("user: ", request.query)
    print("assistant: ", final_message_history[1].dict()['content'])
    memory.save_context({"input": request.query}, {"output": final_message_history[1].dict()['content']})
    print("memory: ", memory.load_memory_variables({})["chat_history"])
    response = final_message_history[1].dict()['content']
    print(f"time taken {time.time()-st}")
    return PlainTextResponse(response)

if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="127.0.0.1", port=6000, reload=True)
