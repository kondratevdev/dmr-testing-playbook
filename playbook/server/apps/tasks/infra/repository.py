from typing import final

import attrs
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.utils import timezone

from server.apps.tasks.logic.value_objects import TaskCreatePayload
from server.apps.tasks.models import Task


@final
@attrs.define(slots=True, frozen=True)
class TaskRepository:
    """Persist and load ``Task`` models."""

    def create(self, payload: TaskCreatePayload, owner: User) -> Task:
        """Create a new incomplete task."""
        return Task.objects.create(
            title=payload.title,
            description=payload.description,
            owner=owner,
        )

    def get(
        self,
        task_id: int,
        owner: User,
        *,
        for_update: bool = False,
    ) -> Task:
        """Get a task, optionally locking its row in an active transaction."""
        tasks = Task.objects.filter(owner=owner)
        if for_update:
            tasks = tasks.select_for_update()
        return tasks.get(pk=task_id)

    def list_for_owner(
        self,
        owner: User,
        *,
        is_completed: bool | None,
    ) -> QuerySet[Task]:
        """Return only tasks visible to the owner, optionally filtered."""
        tasks = Task.objects.filter(owner=owner)
        if is_completed is not None:
            tasks = tasks.filter(is_completed=is_completed)
        return tasks

    def complete(self, task: Task) -> Task:
        """Persist the completed state of a task."""
        task.is_completed = True
        task.completed_at = timezone.now()
        task.save(update_fields=['is_completed', 'completed_at'])
        return task
