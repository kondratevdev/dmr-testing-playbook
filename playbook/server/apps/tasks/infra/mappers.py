from typing import final

import attrs

from server.apps.tasks.logic.value_objects import TaskFullPayload
from server.apps.tasks.models import Task


@final
@attrs.define(slots=True, frozen=True)
class TaskMapper:
    """Map a ``Task`` Django model to its response representation."""

    def __call__(self, task: Task) -> TaskFullPayload:
        """Create a public representation of a task."""
        return TaskFullPayload(
            id=task.pk,
            title=task.title,
            description=task.description,
            is_completed=task.is_completed,
            created_at=task.created_at,
            completed_at=task.completed_at,
        )
