import os
import yaml
import argo_workflows
from argo_workflows.api import workflow_service_api
from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow_create_request import (
    IoArgoprojWorkflowV1alpha1WorkflowCreateRequest,
)

ARGO_SERVER_HOST = os.environ.get('ARGO_SERVER_HOST')
ARGO_SERVER_PORT = os.environ.get('ARGO_SERVER_PORT')
ARGO_TOKEN = os.environ.get('ARGO_TOKEN')

ARGO_CONFIG = argo_workflows.Configuration(host=f"http://{ARGO_SERVER_HOST}:{ARGO_SERVER_PORT}")
ARGO_CONFIG.verify_ssl = False

def run_workflow():
    with open('s3-workflow.yaml', 'r') as f:
        manifest = yaml.safe_load(f)
    api_client = argo_workflows.ApiClient(ARGO_CONFIG)
    api_client.configuration.api_key['BearerToken'] = ARGO_TOKEN
    api_instance = workflow_service_api.WorkflowServiceApi(api_client)
    api_instance.create_workflow(
        namespace="default",
        body=IoArgoprojWorkflowV1alpha1WorkflowCreateRequest(workflow=manifest, _check_type=False),
        _check_return_type=False)
    
if __name__ == '__main__':
    run_workflow()