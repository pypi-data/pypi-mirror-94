"""
Abstraction layer to construct a workflow using and airflow DAG
"""
import json
from os import environ
from pathlib import Path
from typing import Optional
from typing import Union

from airflow import DAG
from airflow.utils.dates import days_ago

from dkist_processing_core._node import Node
from dkist_processing_core._node import task_type_hint
from dkist_processing_core._node import upstreams_type_hint

__all__ = ["Workflow"]


class Workflow:
    """
    Abstraction to create a workflow in the implemented engine api (airflow)
    """

    def __init__(
        self,
        workflow_package: str,
        workflow_name: str,
        workflow_version: Optional[str] = None,
    ):
        self.workflow_package = workflow_package
        self.workflow_name = workflow_name
        self.workflow_version = workflow_version or environ.get("BUILD_VERSION", "dev")
        self._dag_name = f"{self.workflow_name}_{self.workflow_version}"
        self._dag = eval(self._dag_definition)
        self.nodes = []

    @property
    def _instrument_name(self) -> str:
        instrument = self.workflow_name.split("_")[0]
        if instrument == self.workflow_name:  # unexpected format
            return "InstrumentUnknown"
        return instrument

    @property
    def _calibration_name(self) -> str:
        calibration = "_".join(self.workflow_name.split("_")[1:])
        if calibration == "":  # unexpected format
            return "CalibrationUnknown"
        return calibration

    @property
    def _dag_tags(self) -> str:
        tags = [self._instrument_name, self._calibration_name, self.workflow_version]
        return json.dumps(tags)

    @property
    def _dag_definition(self):
        return f"DAG(dag_id='{self._dag_name}', start_date=days_ago(2), schedule_interval=None, catchup=False, tags={self._dag_tags})"

    def add_node(
        self,
        task: task_type_hint,
        upstreams: upstreams_type_hint = None,
    ):
        """
        Add a node and edges from that node to the workflow
        """
        node = Node(
            workflow_name=self.workflow_name,
            workflow_version=self.workflow_version,
            workflow_package=self.workflow_package,
            task=task,
            upstreams=upstreams,
        )
        self.nodes.append(node)
        self._dag.add_task(node.operator)
        for upstream, downstream in node.dependencies:
            self._dag.set_dependency(upstream, downstream)

    def load(self):
        """
        Retrieve the native engine (airflow) workflow object
        """
        return self._dag

    def export(self, export_path: Optional[Union[str, Path]] = None) -> Path:
        """
        Write a file representation of the workflow which can be
            run independently of the task dependencies
        """
        export_path = export_path or "export/"
        export_path = Path(export_path)
        export_path.mkdir(exist_ok=True)
        workflow_py = export_path / f"{self._dag_name}.py"

        with workflow_py.open(mode="w") as f:
            f.write(
                f"#  {self.workflow_name} workflow version {self.workflow_version} definition rendered for airflow scheduler\n"
            )
            f.write(self._workflow_imports)
            f.write("# Workflow\n")
            f.write(self._workflow_instantiation)
            f.write("# Nodes\n")
            for n in self.nodes:
                operator = f"{n.task.__name__.lower()}_operator"
                f.write(f"{operator} = {n.operator_definition}")
                f.write(f"d.add_task({operator})\n")
                f.write("\n")
            f.write("# Edges\n")
            f.write(self._workflow_edges)
            f.write("\n")
        return workflow_py

    @property
    def _workflow_imports(self):
        imports = [
            "from datetime import timedelta",
            "from functools import partial",
            "",
            "from airflow import DAG",
            "from airflow.operators.bash import BashOperator",
            "from airflow.utils.dates import days_ago",
            "",
            "from dkist_processing_core._failure_callback import chat_ops_notification",
            "",
            "",
        ]
        return "\n".join(imports)

    @property
    def _workflow_instantiation(self):
        return f"d = {self._dag_definition}\n"

    @property
    def _workflow_edges(self):
        edges = []
        for n in self.nodes:
            for upstream, downstream in n.dependencies:
                edges.append(f"d.set_dependency('{upstream}', '{downstream}')")
        return "\n".join(edges)

    def __repr__(self):
        return f"Workflow(workflow_name={self.workflow_name}, workflow_version={self.workflow_version})"

    def __str__(self):
        return repr(self)
