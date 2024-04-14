from pydantic import BaseModel
from typing import List, Optional, Tuple
from fastapi import APIRouter, Request, UploadFile, File, HTTPException, status
from fastapi.responses import StreamingResponse

from llama_index.core.llms import ChatMessage, MessageRole
from app.engine.index import get_index

from app.engine.loaders.file import get_file_documents, FileLoaderConfig

import os

from app.core.prompts import Prompts

from app.core.llm import TogetherChat

chat_router = r = APIRouter()

# ** TYPES **

class _Message(BaseModel):
    role: MessageRole
    content: str


class _ChatData(BaseModel):
    messages: List[_Message]


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
async def chat(request: Request, data: _ChatData, file: UploadFile = File(...)):

    # ** Input Parser **
    last_message, history = await parse_chat_data(data)

    # ** Document Content **
    data_dir = "tmp"
    file_path = os.path.join(data_dir, file.filename)

    with open(file_path, "wb") as temp_file:
        contents = await file.read()
        temp_file.write(contents)

    config = FileLoaderConfig(
        data_dir=file_path,
        use_llama_parse=False,
        use_unstructured=True
    )
    
    try:
        documents = get_file_documents(config)
        content = documents[0].get_content()

        formatted_prompt_keywords = Prompts.formatPromptKeywords(last_message, content)

        llm = TogetherChat()

        keywords = llm.run(formatted_prompt_keywords)

        index = get_index()

        retriver = index.as_retriever()

        nodes = retriver.retrieve(keywords)

        # TODO: Implement a parser to get content and metadata for every node
        context = [node.get_content() for node in nodes]

        formatted_prompt_analyst = Prompts.formatPromptAnalyst(last_message, context, content)

        response = await llm.run_chat(formatted_prompt_analyst, history)

        async def event_generator():
            async for token in response:
                if await request.is_disconnected():
                    break
                yield token
        
        return StreamingResponse(event_generator(), media_type="text/plain")

    except:
        print('An exception occurred')
