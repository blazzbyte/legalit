from llama_index.llms.together import TogetherLLM

class TogetherChat:
    def __init__(self, generative_model="mistralai/Mixtral-8x7B-Instruct-v0.1", temperature=0.8, max_tokens=256, top_p=0.7, top_k=50, is_chat_model=False):
        self.generative_model = generative_model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.top_k = top_k
        self.is_chat_model = is_chat_model
    
    def _completion_to_prompt(self, completion: str) -> str:
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

        response = llm.complete(query)
        return response
    
    def run_chat(self, query: str):
        pass