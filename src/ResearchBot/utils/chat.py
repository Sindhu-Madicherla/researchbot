from openai import OpenAI
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
)
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_user_message_param import (
    ChatCompletionUserMessageParam,
)
from openai.types.chat.chat_completion_system_message_param import (
    ChatCompletionSystemMessageParam,
)
from typing import Optional, Tuple, List
from .thread import Thread
from ResearchBot.variables.configs import Configs

DEFAULT_SYSTEM_PROMPT = {"role": "system", "content": "You are a helpful assistant"}


class ChatLLM:
    def __init__(self, client: Optional[OpenAI] = None) -> None:
        if client is None:
            self.client = OpenAI()
        else:
            self.client = client

    def chat(
        self,
        messages: List[ChatCompletionMessageParam],
        model: str = Configs.model,
        **kwargs
    ) -> Tuple[ChatCompletionMessageParam, List[ChatCompletionMessageToolCall]]:
        response = self.client.chat.completions.create(
            model=model, messages=messages, **kwargs
        )
        response_message = response.choices[0].message

        return response_message


class ChatSession:
    def __init__(
        self,
        llm: ChatLLM,
        system_prompt: ChatCompletionSystemMessageParam = DEFAULT_SYSTEM_PROMPT,
        default_model: str = Configs.model,
    ) -> None:
        self.llm = llm
        if isinstance(system_prompt, str):
            system_prompt = {"role": "system", "content": system_prompt}
        self.thread = Thread(system_prompt)
        self.default_model = default_model

    def chat(
        self,
        user_message: ChatCompletionUserMessageParam | str | None = None,
        model: str = None,
        **kwargs
    ) -> Tuple[ChatCompletionMessageParam, List[ChatCompletionMessageToolCall]]:

        if model is None:
            model = self.default_model

        # If user_message is not None, append it to the thread else just chat with the current thread
        if user_message:
            if isinstance(user_message, str):
                user_message = {"role": "user", "content": user_message}

            self.thread.append(user_message)

        response = self.llm.chat(self.thread.messages, model=model, **kwargs)

        self.thread.append(response)
        return response
