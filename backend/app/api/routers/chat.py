from pydantic import BaseModel
from typing import List, Optional, Tuple
from fastapi import APIRouter, Request, UploadFile, File, HTTPException, status, Depends
from fastapi.responses import StreamingResponse

from llama_index.core.llms import ChatMessage, MessageRole
from app.engine.index import get_index

from app.engine.loaders.file import get_file_documents, FileLoaderConfig

import os
import aiohttp
from json import dumps

from app.core.prompts import Prompts

from app.core.llm import TogetherChat

chat_router = r = APIRouter()

# ** TYPES **


class _Message(BaseModel):
    role: MessageRole
    content: str


class _ChatData(BaseModel):
    messages: List[_Message]
    user_id: Optional[str] = None

    @classmethod
    def get_data(cls, messages: List[_Message], data: Optional[dict] = None) -> "_ChatData":
        if data and "user_id" in data:
            return cls(messages=messages, user_id=data["user_id"])
        else:
            return cls(messages=messages)


async def parse_chat_data(data: _ChatData) -> Tuple[str, List[ChatMessage]]:
    # check preconditions and get last message
    if len(data.messages) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No messages provided",
        )
    last_message = data.messages.pop()
    if last_message.role != MessageRole.USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last message must be from user",
        )
    # convert messages coming from the request to type ChatMessage
    messages = [
        ChatMessage(
            role=m.role,
            content=m.content,
        )
        for m in data.messages
    ]
    return last_message.content, messages


# ** ROUTES **
@r.post("")
async def chat(request: Request, data: _ChatData = Depends(_ChatData.get_data)):
    # ** Input Parser **
    last_message, history = await parse_chat_data(data)

    if data.user_id:
        # ** Document Content **
        data_dir = data.user_id

        config = FileLoaderConfig(
            data_dir=data_dir,
            use_llama_parse=True,
            use_unstructured=False,
            user_id=data.user_id
        )

        documents = get_file_documents(config)
        content = ''

        for document in documents:
            content += document.get_content()

        formatted_prompt_keywords = Prompts.formatPromptKeywords(
            last_message, content)

    else:
        formatted_prompt_keywords = Prompts.formatPromptKeywords(last_message)

    llm = TogetherChat()

    keywords = llm.run(formatted_prompt_keywords)
    print(keywords)

    index = get_index()

    retriver = index.as_retriever(similarity_top_k=10)

    nodes = retriver.retrieve(keywords)

    # TODO: Implement a parser to get content and metadata for every node
    context = [node.text for node in nodes]
    metadata = [node.metadata for node in nodes]

    if data.user_id:
        formatted_prompt_analyst = Prompts.formatPromptAnalyst(
            last_message, context, content)
    else:
        formatted_prompt_analyst = Prompts.formatPromptAnalyst(
            last_message, context)

    response = llm.run_chat(formatted_prompt_analyst, history)

    async def event_generator():
        for token in response:
            if await request.is_disconnected():
                break
            yield token.delta
        yield dumps(metadata, indent=2)

    return StreamingResponse(event_generator(), media_type="text/plain")
