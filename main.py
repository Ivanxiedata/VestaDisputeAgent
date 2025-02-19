import subprocess
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from css.pages_styling import landing_page_style, smart_contract_page_style, dispute_page_style
app = FastAPI()

# Global dictionary to track running agent processes.
agent_processes = {}

def start_agent(agent_name: str, agent_file: str, port: str):
    """
    Start a Chainlit agent on a specific port if it is not already running.
    """
    process = agent_processes.get(agent_name)
    if process is None or process.poll() is not None:
        # Launch the Chainlit agent using the CLI and specify the port.
        process = subprocess.Popen(["chainlit", "run", agent_file, "--port", port])
        agent_processes[agent_name] = process

@app.get("/", response_class=HTMLResponse)
async def home():
    return landing_page_style

@app.get("/smart_contract", response_class=HTMLResponse)
async def smart_contract():
    # Launch the smart contract agent on port 8002.
    start_agent("smart_contract", "agents/smart_contract_agent.py", "8002")
    return smart_contract_page_style

@app.get("/dispute", response_class=HTMLResponse)
async def dispute():
    # Launch the dispute agent on port 8003.
    start_agent("dispute", "agents/text_reader_dispute_agent.py", "8003")
    return dispute_page_style

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
