from pathlib import Path
from typing import List, Set, Pattern, Optional

from .task import Task


class Selection:
    """Object used for selecting tasks."""

    def __init__(self,
                 ids: Optional[Set[int]] = None,
                 name: Optional[Pattern[str]] = None,
                 states: Set[str] = set(),
                 folders: List[Path] = [],
                 recursive: bool = True,
                 error: Optional[Pattern[str]] = None):
        """Selection.

        Selections is based on:

            ids

        or:

            any combination of name, state, folder and error message.

        Use recursive=True to allow for tasks inside a folder.
        """

        self.ids = ids
        self.name = name
        self.states = states
        self.folders = folders
        self.recursive = recursive
        self.error = error

    def __repr__(self) -> str:
        return (f'Selection({self.ids}, {self.name}, {self.states}, '
                f'{self.folders}, {self.recursive}, {self.error})')

    def select(self, tasks: List[Task]) -> List[Task]:
        """Filter tasks acording to selection object."""
        if self.ids is not None:
            return [task for task in tasks if task.id in self.ids]

        newtasks = []
        for task in tasks:
            if task.state not in self.states:
                continue
            if self.name and not self.name.fullmatch(task.cmd.name):
                continue
            if not any(task.infolder(f, self.recursive) for f in self.folders):
                continue
            if self.error and not self.error.fullmatch(task.error):
                continue
            newtasks.append(task)

        return newtasks
