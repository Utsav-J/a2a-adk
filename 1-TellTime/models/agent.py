from typing import List
from pydantic import BaseModel

class AgentCapabilities(BaseModel):
    push_notifications:bool = False
    streaming:bool = False
    state_transition_history:bool = False

class AgentSkill(BaseModel):
    id:str
    name:str
    description:str|None = None
    tags:List[str]|None = None
    examples:List[str]|None = None
    inputModes:List[str]|None = None
    outputModes:List[str]|None = None

class AgentCard(BaseModel):
    name:str
    description:str
    url:str
    version:str
    capabilities:AgentCapabilities
    skils:List[AgentSkill]