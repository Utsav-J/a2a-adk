import datetime
from pydantic import BaseModel, Field
from typing import Any, Literal, List
from enum import Enum
from uuid import uuid4

class TextPart(BaseModel):
    type: Literal["text"]="text"
    text:str
Part = TextPart

class Message(BaseModel):
    role: Literal["user","agent"]
    parts = List[Part]

class TaskStatus(BaseModel):
    state:str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)

class Task(BaseModel):
    id:str
    status:str
    history:List[Message]

class TaskIdParams(BaseModel):
    id: str
    metadata: dict[str, Any] | None = None

class TaskQueryParams(TaskIdParams):
    history_length:int|None =None

class TaskSendParams(BaseModel):
    id:str
    session_id:str = Field(default_factory=lambda: uuid4.hex)
    message:Message
    history_length:int|None = None
    metadata:dict[str,Any] | None = None


class TaskState(str, Enum):
    SUBMITTED = "submitted"              # Task has been received
    WORKING = "working"                  # Task is in progress
    INPUT_REQUIRED = "input-required"    # Agent is waiting for more input
    COMPLETED = "completed"             # Task is done
    CANCELED = "canceled"               # Task was canceled by user or system
    FAILED = "failed"                   # Something went wrong
    UNKNOWN = "unknown"   
