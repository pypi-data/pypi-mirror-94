"""
This module provides the base class that is used to wrap the various DAG task methods. It
provides support for user-defined setup and cleanup, task monitoring using Elastic APM,
standardized logging and exception handling.
"""
import logging
from abc import ABC
from abc import abstractmethod
from contextlib import contextmanager
from string import ascii_letters
from typing import Optional

import elasticapm
import pkg_resources
from hashids import Hashids

__all__ = ["TaskBase"]

logger = logging.getLogger(__name__)


class ApmTransaction:
    """
    Elastic APM transaction manager for a DAG Task.
        Without configuration it self disables
    """

    def __init__(self, transaction_name: str, apm_client_config: Optional[dict] = None) -> None:
        self.configured = bool(apm_client_config)
        if self.configured:
            self.transaction_name = transaction_name
            self.client = elasticapm.Client(apm_client_config)
            elasticapm.instrument()
            self.client.begin_transaction(self.transaction_name)

    @contextmanager
    def capture_span(self, name: str, *args, **kwargs):
        if not self.configured:
            try:
                yield
            finally:
                pass
        else:
            try:
                with elasticapm.capture_span(name, *args, **kwargs):
                    yield
            finally:
                pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.configured:
            return
        if exc_type:
            self.client.capture_exception()
        self.client.end_transaction(self.transaction_name)
        self.client.close()


class TaskBase(ABC):
    """
    Generic wrapper for the DAG tasks providing a standard interface and execution flow
    Each DAG task must implement its own subclass of this abstract wrapper class.
    Intended instantiation is as a context manager
    >>> class RealTask(TaskBase):
    >>>     def run(self):
    >>>         pass
    >>>
    >>> with RealTask(1, "a", "b") as task:
    >>>     task()
    """

    retries = 3

    def __init__(
        self,
        recipe_run_id: int,
        workflow_name: str,
        workflow_version: str,
        is_task_manual: bool = False,
        apm_client_config: Optional[dict] = None,
    ):
        self.recipe_run_id = int(recipe_run_id)
        self.dataset_id = Hashids(min_length=5, alphabet=ascii_letters).encode(self.recipe_run_id)
        self.workflow_name = workflow_name
        self.workflow_version = workflow_version
        self.is_task_manual = is_task_manual
        self.apm_client_configuration = apm_client_config
        self.task_name = self.__class__.__name__
        logger.info(f"Task {self.task_name} initialized")

    @property
    def library_versions(self):
        """
        Harvest the dependency names and versions from the environment for
          all packages beginning with 'dkist' or are a requirement for a package
          beginning with 'dkist'
        """
        distributions = {d.key: d.version for d in pkg_resources.working_set}
        result = {}
        for pkg in pkg_resources.working_set:
            if pkg.key.startswith("dkist"):
                result[pkg.key] = pkg.version
                for req in pkg.requires():
                    result[req.key] = distributions[req.key]
        return result

    def record_provenance(self):
        """
        Method that can be overridden to record provenance
        """

    @abstractmethod
    def run(self) -> None:
        """
        Abstract method that must be overridden to execute the desired DAG task.
        """

    def __call__(self) -> None:
        """
        The main executable function for the DAG task wrapper. Execution is instrumented with
        Application Performance Monitoring if configured. The standard execution sequence is:\n
        1 run
        2 record provenance

        Returns
        -------
        None
        """

        logger.info(f"Task {self.task_name} started")
        with ApmTransaction(
            transaction_name=self.task_name, apm_client_config=self.apm_client_configuration
        ) as apm:
            with apm.capture_span("Run"):
                self.run()
            with apm.capture_span("Record provenance"):
                self.record_provenance()
        logger.info(f"Task {self.task_name} complete")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Method that can be overridden to execute teardown tasks after task execution
        """

    def __repr__(self):
        return f"{self.__class__.__name__}(recipe_run_id={self.recipe_run_id}, workflow_name={self.workflow_name}, workflow_version={self.workflow_version}, is_task_manual={self.is_task_manual}, apm_client_config={self.apm_client_configuration})"

    def __str__(self):
        return repr(self)
