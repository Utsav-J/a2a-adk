import traceback
from datetime import datetime

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.genai.types import Content,Part
from dotenv import load_dotenv
load_dotenv()

class TellTimeAgent:
    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]
    
    def __init__(self):
        self._agent = self._build_agent()
        self._user_id = "time_agent_user"

        self._runner = Runner(
            app_name=self._agent.name,
            agent=self._agent,
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
            artifact_service=InMemoryArtifactService()
        )

    def _build_agent(self)->LlmAgent:
        return LlmAgent(
            name="TellTimeAgent",
            description="Tells the time, duh",
            model = "gemini-2.0-flash",
            instruction="Reply with the current time in the format YYYY-MM-DD HH:MM:SS"
        )
    
    async def invoke(self, query:str, session_id:str)->str:
        try:
            session = await self._runner.session_service.create_session(
                app_name=self._agent.name,
                user_id = self._user_id,
                state={},
                session_id=session_id
            )

            if session is None:
                session = await self._runner.session_service.create_session(
                    app_name=self._agent.name,
                    user_id=self._user_id,
                    state={},
                    session_id=session_id
                )
            
            content = Content(
                role="user",
                parts=[Part.from_text(text=query)]
            )

            last_event = None
            async for event in self._runner.run_async(
                user_id = self._user_id,
                session_id = session.id,
                new_message = content
            ):
                last_event = event
            
            if not last_event or not last_event.content or not last_event.content.parts:
                return ""
            
            return "\n".join([p.text for p in last_event.content.parts if p.text])
        except Exception as e:
            # Print a user-friendly error message
            print(f"🔥🔥🔥 An error occurred in TellTimeAgent.invoke: {e}")

            # Print the full, detailed stack trace to the console
            traceback.print_exc()

            # Return a helpful error message to the user/client
            return "Sorry, I encountered an internal error and couldn't process your request."


                

    
    async def stream(self,query:str, session_id:str):
        pass