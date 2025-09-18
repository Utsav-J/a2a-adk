from pydantic import BaseModel, Field
from typing import Literal, Any
from uuid import uuid4

class JSONRPCMessage(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    id: int|str|None = Field(default_factory=lambda: uuid4.hex())

class JSONRPCRequest(JSONRPCMessage):
    code: int
    message: str
    data: Any|None = None

class JSONRPCError(BaseModel):
    code: int
    message: str
    data: Any|None = None

class JSONRPCResponse(JSONRPCMessage):
    result: Any|None = None
    error: JSONRPCError|None = None
    
class InternalError(JSONRPCError):
    code: int = -32603
    message:str = "Internal Error"
    data:Any | None = None