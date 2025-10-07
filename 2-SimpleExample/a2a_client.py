import httpx # The modern HTTP client we use for making web requests
import uuid # Used to generate unique IDs for messages and requests
from a2a.client.card_resolver import A2ACardResolver # The tool to find out what an agent can do
from a2a.types import AgentCard, Message, Part, Role, TextPart, SendMessageRequest, MessageSendParams # All the standard A2A data structures
from a2a.client import A2AClient # The main class for talking to the A2A server

BASE_URL = "http://127.0.0.1:9000/" # Where our greeting agent server is running
PUBLIC_AGENT_CARD_PATH=".well-known/agent.json" # The standardized path to find the agent's 'business card'

async def main()->None:
    # We use an async HTTP client for all our communication
    async with httpx.AsyncClient() as httpx_client:
        
        # --- 1. Fetch the Agent Card (The Handshake) ---
        # Initialize the resolver, telling it where the agent lives
        card_resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=BASE_URL
        )

        final_agent_card : AgentCard | None=None

        try:
            print( f"Fetching public agent card from: {BASE_URL}{PUBLIC_AGENT_CARD_PATH}")
            # This makes the GET request to get the agent's capabilities
            _public_card = await card_resolver.get_agent_card()
            final_agent_card_to_use = _public_card
            print("Fetched public agent card")
            print(_public_card.model_dump_json(indent=2))
        except Exception as e:
            print(f"Error fetching public agent card: {e}")
            raise RuntimeError("Failed to fetch public agent card") # Can't talk if we don't know who we're talking to!

        # --- 2. Initialize the A2A Client ---
        # We give the client the agent card so it knows the rules of the road
        client = A2AClient(
            agent_card=final_agent_card_to_use,
            httpx_client=httpx_client
        )
        print("A2AClient initialized")

        # --- 3. Construct the Standardized A2A Message ---
        # Every A2A communication is wrapped in this standard structure
        message = Message(
            role=Role.user, # We are the user, initiating the conversation
            message_id=str(uuid.uuid4()), # Give our message a unique ID
            parts=[
                Part(
                    root=TextPart(text="hey how are you") # The actual text we want to send!
                )
            ]
        )
        
        # Wrap the message in a SendMessageRequest object
        request = SendMessageRequest(
            id=str(uuid.uuid4()), # The overall request needs a unique ID too
            params=MessageSendParams(
                message=message,
            ),
        )

        # --- 4. Send the Request and Get the Response ---
        print("Sending message")
        
        # This sends the message payload to the server's execute endpoint
        response = await client.send_message(request)
        
        # Print the final, standardized A2A response from the agent
        print("Response:")
        print(response.model_dump_json(indent=2))

if __name__ == "__main__":
    import asyncio

    # Gotta run the async main function!
    asyncio.run(main())