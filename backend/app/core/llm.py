from llama_index.llms.together import TogetherLLM
from llama_index.core.llms import ChatMessage, MessageRole

from typing import Sequence


class TogetherChat:
    # ** Init **
    def __init__(self, generative_model="mistralai/Mixtral-8x22B-Instruct-v0.1", temperature=0.8, max_tokens=8000, top_p=0.7, top_k=50, is_chat_model=False):
        self.generative_model = generative_model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.top_k = top_k
        self.is_chat_model = is_chat_model

    # ** LLM Model **

    def run(self, query: str) -> str:

        llm = TogetherLLM(
            self.generative_model,
            temperature=self.temperature,
            max_tokens=40,
            top_p=self.top_p,
            top_k=self.top_k,
            is_chat_model=self.is_chat_model,
        )

        response = llm.complete(query)

        return response.text

    # ** Chat Model **

    def run_chat(self, last_message: str, history: Sequence[ChatMessage]):
        llm = TogetherLLM(
            self.generative_model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            top_k=self.top_k,
            is_chat_model=True
        )

        last_chat_message = ChatMessage(
            role="user", content=last_message)

        messages = history.copy()
        messages.append(last_chat_message)

        return llm.stream_chat(messages)
