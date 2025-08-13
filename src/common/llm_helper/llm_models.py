from enum import Enum, auto


class LLMModel(Enum):
    OPENAI = auto()
    BEDROCK = auto()