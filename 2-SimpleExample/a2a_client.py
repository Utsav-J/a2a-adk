import httpx
import uuid
from a2a.client.card_resolver import A2ACardResolver
from a2a.types import AgentCard, Message, Part, Role, TextPart, SendMessageRequest, MessageSendParams
from a2a.client import A2AClient

BASE_URL = "http://127.0.0.1:9000/"
PUBLIC_AGENT_CARD_PATH=".well-known/agent.json"

async def main()->None:
    async with httpx.AsyncClient() as httpx_client:
        card_resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=BASE_URL
        )

        final_agent_card : AgentCard | None=None

        try:
            print( f"Fetching public agent card from: {BASE_URL}{PUBLIC_AGENT_CARD_PATH}")
            _public_card = await card_resolver.get_agent_card()
            final_agent_card_to_use = _public_card
            print("Fetched public agent card")
            print(_public_card.model_dump_json(indent=2))
        except Exception as e:
            print(f"Error fetching public agent card: {e}")
            raise RuntimeError("Failed to fetch public agent card")

        client = A2AClient(
            agent_card=final_agent_card_to_use,
            httpx_client=httpx_client
        )
        print("A2AClient initialized")

        message = Message(
            role=Role.user,
            message_id=str(uuid.uuid4()),
            parts=[
                Part(
                    root=TextPart(text="hey how are you")
                )
            ]
        )

        request = SendMessageRequest(
            id=str(uuid.uuid4()),
            params=MessageSendParams(
                message=message,
            ),
        )

        print("Sending message")
        
        response = await client.send_message(request)
        print("Response:")
        print(response.model_dump_json(indent=2))

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

