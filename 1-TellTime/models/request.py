from typing import Literal, Annotated, Union
from pydantic import TypeAdapter, Field
from models.json_rpc import JSONRPCRequest, JSONRPCResponse
from models.task import Task, TaskSendParams, TaskQueryParams

class SendTaskRequest(JSONRPCRequest):
    method:Literal["/tasks/send"] = "/tasks/send"
    params:TaskSendParams

class GetTaskRequest(JSONRPCRequest):
    method:Literal["/tasks/get"] = "/tasks/get"
    params:TaskQueryParams

class SendTaskResponse(JSONRPCResponse):
    result:Task|None = None

class GetTaskResponse(JSONRPCResponse):
    result:Task|None=None

A2ARequest = TypeAdapter(
    Annotated[
        Union[SendTaskRequest, GetTaskRequest],
        Field(discriminator="method")
    ]
)
