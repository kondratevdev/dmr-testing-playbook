from typing import final

import attrs
from django.utils import timezone

from server.apps.tasks.logic.value_objects import TaskCreatePayload
from server.apps.tasks.models import Task


@final
@attrs.define(slots=True, frozen=True)
class TaskRepository:
    """Persist and load ``Task`` models."""

    def create(self, payload: TaskCreatePayload) -> Task:
        """Create a new incomplete task."""
        return Task.objects.create(
            title=payload.title,
            description=payload.description,
        )

    def get(self, task_id: int, *, for_update: bool = False) -> Task:
        """Get a task, optionally locking its row in an active transaction."""
        if for_update:
            return Task.objects.select_for_update().get(pk=task_id)
        return Task.objects.get(pk=task_id)

    def complete(self, task: Task) -> Task:
        """Mark a task as complete if it has not been completed yet."""
        if not task.is_completed:
            task.is_completed = True
            task.completed_at = timezone.now()
            task.save(update_fields=['is_completed', 'completed_at'])
        return task
