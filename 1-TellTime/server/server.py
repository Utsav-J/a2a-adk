from datetime import datetime
from models.agent import AgentCard
from agents.adk import task_manager
import json
from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from models.request import A2ARequest, SendTaskRequest
from models.json_rpc import JSONRPCResponse, InternalError
from starlette.requests import Request
from fastapi.encoders import jsonable_encoder
from typing import Optional

def json_serializer(obj):
    """
    This function can convert Python datetime objects to ISO strings.
    If you try to serialize a type it doesn't know, it will raise an error.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

class A2AServer:
    def __init__(self, agent_card: AgentCard,task_manager: task_manager, host="0.0.0.0", port=5000,) -> None:
        self.host = host
        self.port = port
        self.agent_card = agent_card
        self.task_manager = task_manager
        self.app = Starlette()
        self.app.add_route("/",self._handle_request,methods=["POST"])
        self.app.add_route("/.well-known/agent.json", self._get_agent_card, methods=["GET"])
        
    def start(self):
        if not self.agent_card or not self.task_manager:
            raise ValueError("Required fields not found")
        import uvicorn
        uvicorn.run(app=self.app,host=self.host, port=self.port)

    async def _handle_request(self, request:Request)->Response:
        try:
            body = await request.json()
            print("Incoming JSON: \n", json.dumps(body))
            json_rpc = A2ARequest.validate_python(body)

            if isinstance(json_rpc, SendTaskRequest):
                result = await self.task_manager.on_send_task(json_rpc)
            else:
                raise ValueError(f"Unsupported A2A method: {type(json_rpc)}")
            
            return self._create_response(result)
        except Exception as e:
            # Return a JSON-RPC compliant error response if anything fails
            return JSONResponse(
                JSONRPCResponse(id=None, error=InternalError(message=str(e))).model_dump(),
                status_code=400
            )


    async def _get_agent_card(self, request:Request)->Response:
        return JSONResponse(self.agent_card.model_dump(exclude_none=True)) 
    

    def _create_response(self, result):
        if isinstance(result, JSONRPCResponse):
            # jsonable_encoder automatically handles datetime and UUID
            return JSONResponse(content=jsonable_encoder(result.model_dump(exclude_none=True)))
        else:
            raise ValueError("Invalid response type")