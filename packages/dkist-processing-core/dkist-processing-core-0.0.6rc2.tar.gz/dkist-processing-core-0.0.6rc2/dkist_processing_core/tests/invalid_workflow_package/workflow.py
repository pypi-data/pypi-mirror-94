"""
Example invalid workflow
"""
from dkist_processing_core import Workflow
from dkist_processing_core.tests.task_example import Task
from dkist_processing_core.tests.task_example import Task2


# |<--------------------|
# |-->Task -> Task2 --> |


example = Workflow(workflow_name="invalid_workflow", workflow_package=__package__)
example.add_node(task=Task, upstreams=Task2)
example.add_node(task=Task2, upstreams=Task)
