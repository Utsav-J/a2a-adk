from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentSkill, AgentCard
from agent_executor import GreetingAgentExecutor
import uvicorn

import sys
import os
cur_dir = os.path.dirname(__file__)
sys.path.append(cur_dir)

def main():
    skill = AgentSkill(
        id="greeting_agent",
        name = "Greet",
        description="Returns a greeting",
        examples=["Hey","Hello","Heyyyy"],
        tags = ["greeting", "hello", "world"],
    )

    agent_card = AgentCard(
        name="greeting_agent",
        description="Greets the user",
        url="http://127.0.0.1:9000",
        default_input_modes=['text'],
        default_output_modes=['text'],
        skills=[skill],
        capabilities=AgentCapabilities(),
        version="1.0.0",
    )   

    request_handler = DefaultRequestHandler(
        agent_executor=GreetingAgentExecutor(),
        task_store=InMemoryTaskStore()
    )

    server= A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler
    )

    uvicorn.run(server.build(), host="0.0.0.0", port=9000)

if __name__ == "__main__":
    main()

        