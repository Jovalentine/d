from abc import ABC, abstractmethod

class ExtractionEngine(ABC):
    @abstractmethod
    def start_engine(self):
        raise NotImplemented("This method must be implemented in subclass")