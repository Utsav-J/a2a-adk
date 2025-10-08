import httpx
from a2a.types import AgentCard
from a2a.client import A2AClient
from a2a.types import (
    SendMessageRequest,
    SendMessageResponse,
    Task,
    TaskStatusUpdateEvent,
    TaskArtifactUpdateEvent,
)
from typing import Callable
from dotenv import load_dotenv

load_dotenv()


TaskCallbackArg = Task | TaskStatusUpdateEvent | TaskArtifactUpdateEvent
TaskUpdateCallback = Callable[[TaskCallbackArg, AgentCard], Task]
# equivalent of saying this:
# def TaskUpdateCallback(arg: TaskCallbackArg, card: AgentCard) -> Task:


class RemoteAgentConnection:
    def __init__(self, agent_card: AgentCard, agent_url: str) -> None:
        print(f"agent_card: {agent_card}")
        print(f"agent_url: {agent_url}")
        self._httpx_client = httpx.AsyncClient(timeout=30)
        self.agent_client = A2AClient(self._httpx_client, agent_card, url=agent_url)
        self.card = agent_card
        self.conversation_name = None
        self.conversation = None
        self.pending_tasks = set()

    def get_agent(self) -> AgentCard:
        return self.card

    async def send_message(
        self, message_request: SendMessageRequest
    ) -> SendMessageResponse:
        return await self.agent_client.send_message(message_request)
