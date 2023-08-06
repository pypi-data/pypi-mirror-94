# dkist-processing-core

## Overview
The dkist-processing-core package provides an abstraction layer between the dkist data processing code and the workflow
engine that supports it (airflow). By providing the abstraction layer to airflow specifically a versioning system is
implemented.

![Core, Common, and Instrument Brick Diagram](docs/auto_proc_brick.png "Brick Diagram")

There are 3 main entities which implement the abstraction:

*Task* : The Task provides a definition of the dkist data processing task interface.
It additionally implements some methods that should be global for all dkist processing tasks.

*Workflow* : The Workflow defines an api independent of the workflow engine it abstracts.  It also implements the translation to
engine specific workflow definitions.  In the case of airflow this is a DAG.

*Node* : The Node is used by the Workflow to translate a Task to the engine specific implementation of the Task which runs inside of a python virtual environment.
The virtual environment enables the loading of only that tasks dependencies.

Additional support functions are provided in build_utils.

## Usage
The Workflow and Task are the primary objects used by client libraries.
The Task is used as a base class and the subclass must at a minimum implement run.
A Workflow is used to give the tasks an order of execution and a name for the flow.
```python
from dkist_processing_core import TaskBase
from dkist_processing_core import Workflow

# Task definitions
class MyTask1(TaskBase):
    def run(self):
        print("Running MyTask1")


class MyTask2(TaskBase):
    def run(self):
        print("Running MyTask2")

# Workflow definition
# MyTask1 -> MyTask2
w = Workflow(workflow_name="MyWorkflow", workflow_version="dev")
w.add_node(MyTask1, upstreams=None)
w.add_node(MyTask2, upstreams=MyTask1)
```

Using the dkist-processing-core for data processing library/repo with airflow involves a project structure and build process that results in a zip
of code artifacts and a zip of workflow artifacts.

![Build Artifacts Diagram](docs/auto-proc-concept-model.png "Build Artifacts")

The client dkist data processing libraries should implement a structure and build pipeline using [dkist-processing-test](https://bitbucket.org/dkistdc/dkist-processing-test/src/master/)
as an example.  The build pipelines for a client repo can leverage the [build_utils](dkist_processing_core/build_utils.py) for test and export.

Specifically for airflow, the resulting deployment has the versioned workflow artifacts all available to the scheduler
and the versioned code artifacts available to workers for task execution

![Airflow Deployment Diagram](docs/automated-processing-deployed.png "Airflow Deployment")

## Build
dkist-processing-core is built using [bitbucket-pipelines](bitbucket-pipelines.yml)

## Deployment
dkist-processing-core is deployed to [PyPI](https://pypi.org/project/dkist-processing-core/)

### Environment Variables
| VARIABLE      | Description                                                                                                                | Type | default |
|---------------|----------------------------------------------------------------------------------------------------------------------------|------|---------|
| BUILD_VERSION | Build/Export pipelines only.  This is the value that will be appended to all artifacts and represents their unique version | STR  | dev     |
| CODE_MOUNT    | Runtime Environment (e.g. Worker) only.  This is the Base Path the code artifact is deployed to                            | STR  |         |
| MESH_CONFIG   | Provides the dkistdc cloud mesh configuration.  Specifically the location of the message broker                            | JSON |         |
| ISB_USERNAME  | Message broker user name                                                                                                   | STR  |         |
| ISB_PASSWORD  | Message broker password                                                                                                    | STR  |         |

## Development

```bash
git clone git@bitbucket.org:dkistdc/dkist-processing-core.git
cd dkist-processing-core
pre-commit install
pip install -e .[test]
pytest -v --cov dkist_processing_core
```
