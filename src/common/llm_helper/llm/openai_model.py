from typing import Any
from typing_extensions import override
from openai import AzureOpenAI, OpenAI
from .base_model import BaseModel
from dataclasses import dataclass

@dataclass
class OpenAIModel(BaseModel):
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
        if self._llm_params['deployment'] == 'azure':
            self._client = AzureOpenAI(
                azure_endpoint=self._llm_params['endpoint'],
                api_key=self._llm_params['api_key'],
                api_version=self._llm_params['api_version']
            )
        elif self._llm_params['deployment'] == 'public':
            self._client = OpenAI(api_key=self._llm_params['api_key'])
        else:
            raise ValueError('Deployment not supported')

    @override
    def send_message_to_llm(self, message: str, prompt: str):
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": message}
            ],
            response_format={"type": "json_object"},
            timeout=120
        )
        print("prompt", {"role": "system", "content": prompt},
                {"role": "user", "content": message})
        return response.choices[0].message.content
