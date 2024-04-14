from pydantic import BaseModel
from typing import List, Any, Optional, Dict, Tuple
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from llama_index.core.chat_engine.types import (
    BaseChatEngine,
)
from llama_index.core.schema import NodeWithScore
from llama_index.core.llms import ChatMessage, MessageRole
from app.engine import get_chat_engine
from app.engine.index import get_index

chat_router = r = APIRouter()

# ** TYPES **


class _Message(BaseModel):
    role: MessageRole
    content: str


class _ChatData(BaseModel):
    messages: List[_Message]

    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {
                        "role": "user",
                        "content": "What standards for letters exist?",
                    }
                ]
            }
        }

# ** ROUTES **


@r.post("")
async def chat(request: Request, data: _ChatData, chat_engine: BaseChatEngine = Depends(get_chat_engine),):
    try:
        # Query
        query = "" ##get query from request
        # Document
        # TODO:Parser document from file to PDF
        # Retriver
        # TODO: Format prompt, generate keywords list and send it to retrieve documents
        index = get_index()
        retriver = index.as_retriever()
        nodes = retriver.retrieve() ## Send 
        text_nodes = [node.get_content() for node in nodes]
        # Chat
        # TODO: Format prompt and send data and history to ChatModel
        # Return response on streaming
    except:
        print('An exception occurred')
