from pydantic import BaseModel
from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message

class GreetingAgent(BaseModel):
    """Greeting agent that returns a greeting"""

    async def invoke(self) -> str:
        return "Hello there. Greeting agent says hi!"

class GreetingAgentExecutor(AgentExecutor):
    def __init__(self) -> None:
        self.agent = GreetingAgent()

    async def execute(self, context:RequestContext, event_queue:EventQueue):
        result = await self.agent.invoke()
        await event_queue.enqueue_event(new_agent_text_message(result))
    
    async def cancel(self,context: RequestContext, event_queue: EventQueue):
        raise Exception("didnt implement cancel for this one")