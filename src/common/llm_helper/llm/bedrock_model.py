from typing import Any
from typing_extensions import override
import boto3
from .base_model import BaseModel
from dataclasses import dataclass

@dataclass
class BedrockModel(BaseModel):
    _llm_params: dict[str, Any]
    _client = None

    def __post_init__(self):
        if not self._llm_params:
            raise ValueError('llm_params is not set while creating the model')
        self._model = self._llm_params['model']
        self._engine = self._llm_params['engine']
        self._deployment = self._llm_params['deployment']

    @override
    def initialize_client(self):
        self._client = boto3.client("bedrock-runtime", region_name=self._llm_params['region_name'])

    @override
    def send_message_to_llm(self, message: str, prompt: str):
        response = self._client.converse(
            modelId=self._model,
            messages=[
                {"role": "user", "content": [{"text": message}]}
            ],
            system=[
                {'text': prompt},
            ],
            inferenceConfig={"maxTokens": 2000, "temperature": 0.7, "topP": 1},
        )
        return response["output"]["message"]["content"][0]["text"]