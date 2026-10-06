from typing import final


@final
class TaskAlreadyCompletedError(Exception):
    """A completed task cannot be completed again."""
