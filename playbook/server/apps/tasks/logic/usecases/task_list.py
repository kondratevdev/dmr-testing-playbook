from __future__ import annotations

from typing import TYPE_CHECKING, final

import attrs
from django.contrib.auth.models import User

from server.apps.tasks.logic.value_objects import TaskFullPayload

if TYPE_CHECKING:
    from server.apps.tasks.infra import mappers, repository


@final
@attrs.define(slots=True, frozen=True)
class ListTasks:
    """List tasks belonging to the current user."""

    _repository: repository.TaskRepository
    _mapper: mappers.TaskMapper

    def __call__(
        self,
        owner: User,
        *,
        is_completed: bool | None,
    ) -> list[TaskFullPayload]:
        """Apply the filter and map the visible tasks."""
        tasks = self._repository.list_for_owner(
            owner,
            is_completed=is_completed,
        )
        return self._mapper.many(tasks)
