"""
Global test fixtures
"""
from configparser import ConfigParser
from contextlib import contextmanager
from pathlib import Path
from shutil import rmtree
from typing import Any
from typing import List
from typing import Tuple
from typing import Type

import pytest

import dkist_processing_core
from dkist_processing_core import TaskBase
from dkist_processing_core import Workflow
from dkist_processing_core._node import Node
from dkist_processing_core.tests.task_example import Task


@pytest.fixture(scope="module")
def export_path() -> str:
    """
    export path object that will be removed on teardown
    """
    path = Path("export/")
    yield str(path)
    rmtree(path)


@pytest.fixture(scope="session")
def task_subclass():
    """
    Sub class of the abstract task base class implementing methods that are expected to
       be subclassed with inspect-able metadata
    """
    return Task


@pytest.fixture(scope="session")
def error_task_subclass():
    """
    Sub class of the abstract task base class implementing methods that are expected to
       be subclassed with inspect-able metadata
    """

    class Task(TaskBase):
        def __init__(self, *args, **kwargs):
            self.run_was_called = False
            self.record_provenance_was_called = False
            super().__init__(*args, **kwargs)

        def run(self):
            self.run_was_called = True

        def record_provenance(self):
            self.record_provenance_was_called = True
            raise RuntimeError("error recording provenance")

    return Task


@pytest.fixture()
def task_instance(task_subclass):
    """
    Create an instance of the task subclass defined in task_subclass
    """
    with task_subclass(
        recipe_run_id=1, workflow_name="workflow_name", workflow_version="version"
    ) as task:
        yield task


@pytest.fixture()
def package_dependencies() -> set:
    """
    Extract dependencies from setup.cfg and format into a set of package names
    """
    module_path = Path(dkist_processing_core.__path__[0])
    setup_cfg = module_path.parent / "setup.cfg"
    config = ConfigParser()
    config.read(setup_cfg)
    install_requires = [d for d in config["options"]["install_requires"].splitlines() if d]
    requirements = install_requires + ["dkist-processing-core"]
    dependencies = {pkg.split(" ")[0] for pkg in requirements}
    dependencies_without_optionals = {d.split("[")[0] for d in dependencies}
    return dependencies_without_optionals


@pytest.fixture()
def workflow():
    """
    Create an instance of the Workflow abstraction without tasks
    """
    name = "instrument_calibration_name"
    version = "V6-12342"
    workflow_instance = Workflow(
        workflow_name=name, workflow_version=version, workflow_package=__package__
    )
    return workflow_instance, name, version


@pytest.fixture()
def workflow_tasks(task_subclass) -> List[Type[TaskBase]]:
    """
    A list of Tasks that can be composed into a workflow
    """

    class TaskA(task_subclass):
        pass

    class TaskB(task_subclass):
        pass

    class TaskC(task_subclass):
        pass

    class TaskD(task_subclass):
        pass

    return [TaskA, TaskB, TaskC, TaskD]


@pytest.fixture(params=["0_upstream", "1_upstream", "2_upstream"])
def node(workflow_tasks, request) -> Tuple[Node, Type[TaskBase], Any, str, str]:
    """
    Node instance and its component parts
    """
    version = "V6-123"
    name = f"{request.param}_{version}"
    TaskA, TaskB, TaskC, _ = workflow_tasks
    upstreams = {
        "0_upstream": (None, []),
        "1_upstream": (TaskB, [TaskB]),
        "2_upstream": ([TaskB, TaskC], [TaskB, TaskC]),
    }
    upstream = upstreams[request.param]
    package = __package__
    return (
        Node(
            workflow_name=name,
            workflow_version=version,
            workflow_package=package,
            task=TaskA,
            upstreams=upstream[0],
        ),
        TaskA,
        upstream[1],
        name,
        version,
    )


@pytest.fixture()
def fake_producer():
    class FakeProducer:
        @classmethod
        def publish_message(cls, message):
            return message

    return FakeProducer


@pytest.fixture()
def fake_producer_factory(fake_producer):
    @contextmanager
    def fake_factory():
        try:
            yield fake_producer
        finally:
            pass

    return fake_factory
