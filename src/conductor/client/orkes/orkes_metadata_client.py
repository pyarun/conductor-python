from typing import Optional, List
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models.workflow_def import WorkflowDef
from conductor.client.http.models.task_def import TaskDef
from conductor.client.http.models.tag_string import TagString
from conductor.client.orkes.models.metadata_tag import MetadataTag
from conductor.client.orkes.models.ratelimit_tag import RateLimitTag
from conductor.client.metadata_client import MetadataClient
from conductor.client.orkes.orkes_base_client import OrkesBaseClient
from conductor.client.exceptions.api_exception_handler import api_exception_handler, for_all_methods

@for_all_methods(api_exception_handler, ["__init__"])
class OrkesMetadataClient(OrkesBaseClient, MetadataClient):
    def __init__(self, configuration: Configuration):
        super(OrkesMetadataClient, self).__init__(configuration)
        
    def register_workflow_def(self, workflow_def: WorkflowDef, overwrite: Optional[bool] = True):
        self.metadataResourceApi.create(workflow_def, overwrite=overwrite)

    def update_workflow_def(self, workflow_def: WorkflowDef, overwrite: Optional[bool] = True):
        self.metadataResourceApi.update1([workflow_def], overwrite=overwrite)

    def unregister_workflow_def(self, name: str, version: int):
        self.metadataResourceApi.unregister_workflow_def(name, version)

    def get_workflow_def(self, name: str, version: Optional[int] = None) -> WorkflowDef:
        workflow = None
        if version:
            workflow = self.metadataResourceApi.get(name, version=version)
        else:
            workflow = self.metadataResourceApi.get(name)

        return workflow

    def get_all_workflow_defs(self) -> List[WorkflowDef]:
        return self.metadataResourceApi.get_all_workflows()

    def register_task_def(self, task_def: TaskDef):
        self.metadataResourceApi.register_task_def([task_def])

    def update_task_def(self, task_def: TaskDef):
        self.metadataResourceApi.update_task_def(task_def)

    def unregister_task_def(self, task_type: str):
        self.metadataResourceApi.unregister_task_def(task_type)

    def get_task_def(self, task_type: str) -> TaskDef:
        return self.metadataResourceApi.get_task_def(task_type)

    def get_all_task_defs(self) -> List[TaskDef]:
        return self.metadataResourceApi.get_task_defs()
        
    def addWorkflowTag(self, tag: MetadataTag, workflowName: str):
        self.tagsApi.add_workflow_tag(tag, workflowName)

    def deleteWorkflowTag(self, tag: MetadataTag, workflowName: str):
        tagStr = TagString(tag.key, tag.type, tag.value)
        self.tagsApi.delete_workflow_tag(tagStr, workflowName)

    def getWorkflowTags(self, workflowName: str) -> List[MetadataTag]:
        return self.tagsApi.get_workflow_tags(workflowName)

    def setWorkflowTags(self, tags: List[MetadataTag], workflowName: str):
        self.tagsApi.set_workflow_tags(tags, workflowName)

    def addTaskTag(self, tag: MetadataTag, taskName: str):
        self.tagsApi.add_task_tag(tag, taskName)
    
    def deleteTaskTag(self, tag: MetadataTag, taskName: str):
        tagStr = TagString(tag.key, tag.type, tag.value)
        self.tagsApi.delete_task_tag(tagStr, taskName)

    def getTaskTags(self, taskName: str) -> List[MetadataTag]:
        return self.tagsApi.get_task_tags(taskName)
        
    def setTaskTags(self, tags: List[MetadataTag], taskName: str):
        self.tagsApi.set_task_tags(tags, taskName)

    def setWorkflowRateLimit(self, rateLimit: int, workflowName: str):
        self.removeWorkflowRateLimit(workflowName)
        rateLimitTag = RateLimitTag(workflowName, rateLimit)
        self.tagsApi.add_workflow_tag(rateLimitTag, workflowName)

    def getWorkflowRateLimit(self, workflowName: str) -> Optional[int]:
        tags = self.tagsApi.get_workflow_tags(workflowName)
        for tag in tags:
            if tag.type == "RATE_LIMIT" and tag.key == workflowName:
                return tag.value

        return None

    def removeWorkflowRateLimit(self, workflowName: str):
        currentRateLimit = self.getWorkflowRateLimit(workflowName)

        if currentRateLimit:
            rateLimitTag = RateLimitTag(workflowName, currentRateLimit)
            self.tagsApi.delete_workflow_tag(rateLimitTag, workflowName)
