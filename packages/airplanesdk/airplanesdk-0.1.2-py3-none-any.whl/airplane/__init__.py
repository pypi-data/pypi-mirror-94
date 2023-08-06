"""airplane - An SDK for writing Airplane tasks in Python"""

__version__ = "0.1.2"
__author__ = "Airplane <support@airplane.dev>"
__all__ = []

from .client import Airplane

default_client = None


def write_output(self, value):
    """Writes the value to the task's output."""
    _proxy("write_output", value)


def write_named_output(self, name, value):
    """Writes the value to the task's output, tagged by the key."""
    _proxy("write_named_output", name, value)


def run(self, task_id, parameters):
    """Triggers an Airplane task with the provided arguments."""
    _proxy("run", task_id, parameters)


def _proxy(method, *args, **kwargs):
    global default_client
    if not default_client:
        default_client = Airplane()

    fn = getattr(default_client, method)
    fn(*args, **kwargs)
