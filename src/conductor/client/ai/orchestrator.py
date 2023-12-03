from __future__ import annotations

import time
from typing import Optional, List
from uuid import uuid4

from typing_extensions import Self

from conductor.client.ai.integrations import IntegrationConfig
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.api.prompt_resource_api import PromptResourceApi
from conductor.client.http.api.workflow_resource_api import WorkflowResourceApi
from conductor.client.http.api_client import ApiClient
from conductor.client.http.models.integration_api_update import IntegrationApiUpdate
from conductor.client.http.models.integration_update import IntegrationUpdate
from conductor.client.http.models.prompt_template import PromptTemplate
from conductor.client.orkes_clients import OrkesClients
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.task.llm_tasks.llm_text_complete import LlmTextComplete
from conductor.client.workflow.task.llm_tasks.utils.prompt import Prompt
from conductor.client.ai.configuration import AIConfiguration


class AIOrchestrator:
    def __init__(self, api_configuration: Configuration, ai_configuration: AIConfiguration,
                 prompt_test_workflow_name: str = '') -> Self:
        self.ai_configuration = ai_configuration
        orkes_clients = OrkesClients(api_configuration)

        self.integration_client = orkes_clients.get_integration_client()
        self.workflow_client = orkes_clients.get_integration_client()
        self.workflow_executor = orkes_clients.get_workflow_executor()
        self.prompt_client = orkes_clients.get_prompt_client()

        self.prompt_test_workflow_name = prompt_test_workflow_name
        if self.prompt_test_workflow_name == '':
            self.prompt_test_workflow_name = 'prompt_test_' + str(uuid4())

    def add_prompt_template(self, name: str, prompt_template: str, description: str):
        self.prompt_client.save_prompt(name, description, prompt_template)
        return self

    def test_prompt_template(self, name: str, variables: dict,
                             stop_words: Optional[List[str]] = [], max_tokens: Optional[int] = 100,
                             temperature: int = 0,
                             top_p: int = 1):
        prompt = Prompt(name, variables)
        llm_text_complete = LlmTextComplete(
            'prompt_test', 'prompt_test',
            self.ai_configuration.llm_provider, self.ai_configuration.text_complete_model,
            prompt,
            stop_words, max_tokens, temperature, top_p
        )
        name = self.prompt_test_workflow_name
        prompt_test_workflow = ConductorWorkflow(
            executor=self.workflow_executor,
            name=name,
            description='Prompt testing workflow from SDK'
        )
        prompt_test_workflow.add(llm_text_complete)
        output = prompt_test_workflow.execute({})
        if 'result' in output.keys():
            return output['result']
        else:
            return ''

    def add_ai_integration(self, name: str, provider: str, models: List[str], description: str, config: IntegrationConfig):
        details = IntegrationUpdate()
        details.configuration = config.to_dict()
        details.type = provider
        details.category = 'AI_MODEL'
        details.enabled = True
        details.description = description
        self.integration_client.save_integration(name, details)
        for model in models:
            api_details = IntegrationApiUpdate()
            api_details.enabled = True
            api_details.description = description
            self.integration_client.save_integration_api(name, model, api_details)


    def add_vector_store(self, name: str, provider: str, indices: List[str], description: str, api_key: str,
                         config: IntegrationConfig):
        pass

