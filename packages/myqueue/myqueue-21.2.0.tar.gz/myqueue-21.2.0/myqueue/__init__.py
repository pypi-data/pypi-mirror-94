"""Top level module definitions.

The version number and the submit() function is defined here.
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .task import Task  # noqa


__version__ = '21.2.0'


def submit(*tasks: 'Task', verbosity: int = 1, dry_run: bool = False) -> None:
    """Submit tasks.

    Parameters
    ----------
    tasks: List of Task objects
        Tasks to submit.
    verbosity: int
        Must be 0, 1 or 2.
    dry_run: bool
        Don't actually submit the task.
    """
    from .queue import Queue
    from .config import initialize_config
    from pathlib import Path
    initialize_config(Path('.').resolve())
    with Queue(verbosity, dry_run=dry_run) as queue:
        queue.submit(tasks)
