from pydantic import BaseModel
from a2a.server.agent_execution import AgentExecutor # The base class for execution logic
from a2a.server.agent_execution.context import RequestContext # Holds info about the request
from a2a.server.events import EventQueue # The mechanism to send messages back to the client
from a2a.utils import new_agent_text_message # A handy helper to quickly format a text response

class GreetingAgent(BaseModel):
    """Greeting agent that returns a greeting"""

    # This is the actual agent's core logic.
    # In a real app, this is where the complex LLM or AI code would live!
    async def invoke(self) -> str:
        return "Hello there. Greeting agent says hi!"

class GreetingAgentExecutor(AgentExecutor):
    """
    The Executor wraps the actual agent, making it A2A compliant.
    It defines the standard execute and cancel methods for the server to use.
    """
    def __init__(self) -> None:
        # We hold an instance of our simple agent
        self.agent = GreetingAgent()

    # The main function the A2A server calls when a client sends a message
    async def execute(self, context:RequestContext, event_queue:EventQueue):
        # 1. Call the underlying agent's logic to get the result
        result = await self.agent.invoke()
        
        # 2. Format the result into a standardized A2A message and put it on the queue.
        # This queue handles sending the message back to the client!
        await event_queue.enqueue_event(new_agent_text_message(result))
    
    # Required for the Executor interface, but we keep it simple for this example
    async def cancel(self,context: RequestContext, event_queue: EventQueue):
        raise Exception("didnt implement cancel for this one") 