from typing import Any
from .llm.base_model import BaseModel
from .llm.bedrock_model import BedrockModel
from .llm.openai_model import OpenAIModel
from .llm_models import LLMModel


class LLMModelFactory:

    def get_llm_model(self, llm_model: LLMModel, llm_params: dict[str, Any]) -> BaseModel:
        if llm_model == LLMModel.OPENAI:
            model = OpenAIModel(llm_params)
        elif llm_model == LLMModel.BEDROCK:
            model = BedrockModel(llm_params)
        else:
            raise ValueError('Unknown llm_model: {}'.format(llm_model))
        model.initialize_client()
        return model
