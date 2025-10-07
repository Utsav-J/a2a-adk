from a2a.server.apps import A2AStarletteApplication # Our friendly Starlette-based A2A server app
from a2a.server.request_handlers import DefaultRequestHandler # Handles incoming A2A messages and routing
from a2a.server.tasks import InMemoryTaskStore # Simple way to track tasks (though ours are super fast)
from a2a.types import AgentCapabilities, AgentSkill, AgentCard # Essential A2A standard types for defining agents
from agent_executor import GreetingAgentExecutor # This is where the actual 'thinking' logic lives (our dummy one!)
import uvicorn # The ASGI server that actually runs our application

import sys
import os
cur_dir = os.path.dirname(__file__)
sys.path.append(cur_dir)

def main():
    # --- 1. Define what our agent can do: The AgentSkill is like a specific function ---
    skill = AgentSkill(
        id="greeting_agent", # A unique ID for this one skill
        name = "Greet", # A friendly name for the skill
        description="Returns a greeting", # Simple explanation!
        examples=["Hey","Hello","Heyyyy"], # Some examples of how to ask for a greeting
        tags = ["greeting", "hello", "world"], # Helpful tags for discovery
    )

    # --- 2. Create the AgentCard: This is the agent's 'business card' ---
    agent_card = AgentCard(
        name="greeting_agent", # The overall name of our agent
        description="Greets the user", # What the agent is generally for
        url="http://127.0.0.1:9000", # Where clients can find this agent (very important!)
        default_input_modes=['text'], # It expects text input
        default_output_modes=['text'], # And it sends back text output
        skills=[skill], 
        capabilities=AgentCapabilities(), # Default capabilities for now
        version="1.0.0", 
    )   

    # --- 3. Set up the A2A Request Handler and Task Store ---
    request_handler = DefaultRequestHandler(
        agent_executor=GreetingAgentExecutor(), # Hooking up our agent's execution logic
        task_store=InMemoryTaskStore() # Using a simple in-memory storage for task management
    )

    # --- 4. Instantiate the A2A Server Application ---
    server= A2AStarletteApplication(
        agent_card=agent_card, # Giving the app its official business card
        http_handler=request_handler # Giving it the brains for handling requests
    )

    # --- 5. Start the Server using Uvicorn! ---
    # Runs the server forever, listening for client requests on port 9000
    uvicorn.run(server.build(), host="0.0.0.0", port=9000)

if __name__ == "__main__":
    main()