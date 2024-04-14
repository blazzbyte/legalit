from llama_index.llms.together import TogetherLLM
from llama_index.core.llms import ChatMessage, MessageRole

from typing import Sequence


class TogetherChat:
    # ** Init **
    def __init__(self, generative_model="mistralai/Mixtral-8x7B-Instruct-v0.1", temperature=0.8, max_tokens=256, top_p=0.7, top_k=50, is_chat_model=False):
        self.generative_model = generative_model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.top_k = top_k
        self.is_chat_model = is_chat_model

    # ** LLM Model **

    def _completion_to_prompt(completion: str) -> str:
        return f"<s>[INST] {completion} [/INST] </s>\n"

    def run(self, query: str):

        llm = TogetherLLM(
            self.generative_model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            top_k=self.top_k,
            is_chat_model=self.is_chat_model,
            completion_to_prompt=self._completion_to_prompt
        )

        return llm.complete(query)
    
    # ** Chat Model **

    def _messages_to_prompt(messages: Sequence[ChatMessage]) -> str:
        """Convert messages to a prompt string."""
        string_messages = []
        for message in messages:
            role = message.role
            content = message.content
            string_message = f"{role.value}: {content}"

            addtional_kwargs = message.additional_kwargs
            if addtional_kwargs:
                string_message += f"\n{addtional_kwargs}"
            string_messages.append(string_message)

        string_messages.append(f"{MessageRole.ASSISTANT.value}: ")
        return "\n".join(string_messages)

    def run_chat(self, last_message: str, history: Sequence[ChatMessage]):
        llm = TogetherLLM(
            self.generative_model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            top_k=self.top_k,
            is_chat_model=self.is_chat_model,
            messages_to_prompt=self._messages_to_prompt
        )

        last_chat_message = ChatMessage(MessageRole.USER, last_message)

        messages = [history, last_chat_message]

        return llm.stream_chat(messages)
