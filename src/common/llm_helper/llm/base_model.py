from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def initialize_client(self):
        raise NotImplemented("This method must be implemented in subclass")

    @abstractmethod
    def send_message_to_llm(self, message: str, prompt: str):
        raise NotImplemented("This method must be implemented in subclass")