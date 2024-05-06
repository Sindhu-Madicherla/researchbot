from pydantic import validate_call
from typing import List
from pydantic import validate_call
from typing import List
from openai.types.chat.chat_completion import ChatCompletionMessage
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_system_message_param import ChatCompletionSystemMessageParam

class Thread:
    @validate_call
    def __init__(self, system_prompt: ChatCompletionSystemMessageParam) -> None:
        self._messages: List[ChatCompletionMessageParam] = []
        self.set_system_prompt(system_prompt)

    @property
    def messages(self) -> List[ChatCompletionMessageParam]:
        return self._messages

    @messages.setter
    @validate_call
    def messages(self, messages: List[ChatCompletionMessageParam]) -> None:
        self._messages = messages

    @validate_call
    def set_system_prompt(self, system_prompt: ChatCompletionSystemMessageParam) -> None:
        """Add or update the system prompt"""
        if self.messages and self.messages[0]['role'] == "system":
            self.messages[0] = system_prompt
        else:
            self.messages.insert(0, system_prompt)

    @validate_call
    def append(self, message: ChatCompletionMessageParam | ChatCompletionMessage) -> None:
        """Add a message to the thread"""
        self.messages.append(message)

    @validate_call
    def extend(self, messages: List[ChatCompletionMessageParam]) -> None:
        """Append multiple messages to the thread"""
        self.messages.extend(messages)

    def pop(self) -> ChatCompletionMessageParam:
        """Remove and return the last message from the thread"""
        return self.messages.pop()