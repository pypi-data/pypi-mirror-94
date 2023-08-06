"""
Tests for the Workflow abstraction
"""
from typing import Callable

import pytest
from airflow import DAG

from dkist_processing_core import Workflow


def test_workflow_metadata(workflow):
    """
    Given: A workflow instance
    When: accessing attributes
    Then: Tha values are properly assigned
    """
    workflow_instance, name, version = workflow

    instrument = name.split("_")[0]
    calibration = "_".join(name.split("_")[1:])

    assert workflow_instance.workflow_name == name
    assert workflow_instance.workflow_version == version
    assert workflow_instance.workflow_package.startswith(__package__.split(".")[0])
    assert workflow_instance.nodes == []
    assert isinstance(workflow_instance._dag, DAG)
    assert workflow_instance._dag.dag_id == f"{name}_{version}"
    assert workflow_instance._instrument_name == instrument
    assert workflow_instance._calibration_name == calibration
    assert workflow_instance._dag_tags == f'["{instrument}", "{calibration}", "{version}"]'


def test_workflow_bad_metadata():
    """
    Given: Workflow Class
    When: Instance is created with non-convention workflow name
    Then: Tags are expected unknown variants
    """
    name = "badname"
    w = Workflow(workflow_name=name, workflow_package=__package__)
    assert w._instrument_name == "InstrumentUnknown"
    assert w._calibration_name == "CalibrationUnknown"


def test_workflow_add_node(workflow_tasks, workflow):
    """
    Given: A set of tasks and a workflow instance
    When: Adding the tasks to the workflow in the
      structure of A >> [B, C] >> D
    Then: the dag object owned by the workflow has the right structure
    """
    workflow_instance, name, version = workflow
    TaskA, TaskB, TaskC, TaskD = workflow_tasks
    task_definitions = {
        TaskA: None,  # none
        TaskB: TaskA,  # single
        TaskC: TaskA,  # single
        TaskD: [TaskB, TaskC],  # list
    }
    task_upstream_expectations = {
        TaskA.__name__: set(),
        TaskB.__name__: {
            TaskA.__name__,
        },
        TaskC.__name__: {
            TaskA.__name__,
        },
        TaskD.__name__: {
            TaskB.__name__,
            TaskC.__name__,
        },
    }
    for task, upstream in task_definitions.items():
        workflow_instance.add_node(task, upstreams=upstream)

    dag = workflow_instance.load()
    assert dag.task_count == 4
    assert len(workflow_instance.nodes) == 4

    for task in dag.tasks:
        assert task.dag_id == f"{name}_{version}"
        assert task.upstream_task_ids == task_upstream_expectations[task.task_id]


def test_invalid_workflow_add_node(workflow):
    """
    Given: An invalid task (not inheriting from TaskBase)and a workflow instance
    When: Adding the task to the workflow
    Then: Get a TypeError
    """
    workflow_instance, _, _ = workflow

    class Task:
        pass

    with pytest.raises(TypeError):
        workflow_instance.add_node(Task)


@pytest.mark.parametrize(
    "func, attr",
    [
        pytest.param(repr, "__repr__", id="repr"),
        pytest.param(str, "__str__", id="str"),
    ],
)
def test_tag_db_dunder(workflow, func: Callable, attr):
    """
    Given: Connection to a tag database
    When: retrieving dunder method that should be implemented
    Then: It is implemented
    """
    workflow_instance, _, _ = workflow

    assert getattr(workflow_instance, attr, None)
    assert func(workflow_instance)
