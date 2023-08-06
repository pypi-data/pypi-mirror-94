"""
Tests for the TaskBase functionality
"""
import pytest
from hypothesis import given
from hypothesis.strategies import integers

from dkist_processing_core.task import TaskBase


@given(id_x=integers(min_value=1), id_y=integers(min_value=1))
def test_dataset_id_uniquely_generated_from_recipe_run_id(task_subclass, id_x, id_y):
    """
    Given: 2 integers > 0
    When: 2 tasks are created using the integers for each of the tasks
    Then: The dataset_id for each class compares the same as the integers compare
       e.g. (1 == 1) is (dataset_id(1) == dataset_id(1))  : True is True
       e.g. (1 == 2) == (dataset_id(1) == dataset_id(2))  : False is False
    """
    expected = id_x == id_y
    task_x = task_subclass(recipe_run_id=id_x, workflow_name="", workflow_version="")
    task_y = task_subclass(recipe_run_id=id_y, workflow_name="", workflow_version="")
    actual = task_x.dataset_id == task_y.dataset_id
    assert expected is actual


@given(id_x=integers(min_value=1))
def test_dataset_id_from_recipe_run_id_produces_the_same_value(task_subclass, id_x):
    """
    Given: an integer > 0
    When: 2 tasks are created using the same integer for each of the tasks
    Then: The dataset_id for each class are equal
    """
    task_1 = task_subclass(recipe_run_id=id_x, workflow_name="", workflow_version="")
    task_2 = task_subclass(recipe_run_id=id_x, workflow_name="", workflow_version="")
    assert task_1.dataset_id == task_2.dataset_id


@pytest.mark.parametrize(
    "apm_client_config",
    [
        pytest.param(None, id="NoAPM"),
        pytest.param(
            {
                "SERVICE_NAME": "test_task",  # Name of dag
                "ENVIRONMENT": "test",
                "SERVER_URL": "http://not.gonna.work.doc/",
            },
            id="NoAPM",
        ),
    ],
)
def test_task_execution(task_subclass, apm_client_config):
    """
    Given: Task subclass and parametrized APM configurations
    When: calling the instance
    Then: the run method is executed
    """
    task = task_subclass(
        recipe_run_id=1, workflow_name="", workflow_version="", apm_client_config=apm_client_config
    )
    task()
    assert task.run_was_called
    assert task.record_provenance_was_called


@pytest.mark.parametrize(
    "apm_client_config",
    [
        pytest.param(None, id="NoAPM"),
        pytest.param(
            {
                "SERVICE_NAME": "test_task",  # Name of dag
                "ENVIRONMENT": "test",
                "SERVER_URL": "http://not.gonna.work.doc/",
            },
            id="NoAPM",
        ),
    ],
)
def test_task_run_failure(error_task_subclass, apm_client_config):
    """
    Given: Task subclass and parametrized APM configurations
    When: calling the instance
    Then: the run method is executed
    """
    task = error_task_subclass(
        recipe_run_id=1, workflow_name="", workflow_version="", apm_client_config=apm_client_config
    )
    with pytest.raises(RuntimeError):
        task()


def test_base_task_instantiation():
    """
    Given: Abstract Base Class for a Task
    When: Instantiating base class
    Then: Receive TypeError
    """
    with pytest.raises(TypeError):
        t = TaskBase(recipe_run_id=1, workflow_name="", workflow_version="")


def test_task_subclass_instantiation(task_subclass):
    """
    Given: Subclass that implements abstract base task method(s)
    When: Instantiating subclass
    Then: Instance and Class attributes are set
    """
    recipe_run_id = 1
    workflow_name = "r2"
    workflow_version = "d2"
    is_task_manual = True
    apm_client_configuration = {
        "SERVICE_NAME": "test_task",
        "ENVIRONMENT": "test",
        "SERVER_URL": "http://not.gonna.work.doc/",
    }
    task = task_subclass(
        recipe_run_id=recipe_run_id,
        workflow_name=workflow_name,
        workflow_version=workflow_version,
        apm_client_config=apm_client_configuration,
        is_task_manual=is_task_manual,
    )
    # class vars
    assert task.retries == task_subclass.retries
    # instance vars
    assert task.recipe_run_id == recipe_run_id
    assert task.workflow_name == workflow_name
    assert task.workflow_version == workflow_version
    assert task.apm_client_configuration == apm_client_configuration
    assert task.is_task_manual == is_task_manual
    # calculated instance vars
    assert task.dataset_id
    assert task.task_name == task_subclass.__name__


def test_library_versions(task_instance, package_dependencies):
    """
    Given: An instance of a TaskBase subclass
    When: accessing library_versions attr
    Then: Result contains the dkist-processing-core package and packages specified in setup.cfg
      - options.install_requires
      - options.extras_require.test
      Result does not contain any other packages
      Result structure is Dict[str,str] where the key is library name and value is the version
    """
    library_names = task_instance.library_versions.keys()
    assert len(library_names) == len(set(library_names))  # no duplicates
    assert set(library_names) == package_dependencies  # only expected packages
    library_versions = task_instance.library_versions.values()
    assert all(library_versions)  # values for all versions


def test_repr_str(task_instance):
    """
    Given:  An instance of a task
    When: accessing the string or repr
    Then: Receive a value
    """
    assert str(task_instance)
    assert repr(task_instance)
