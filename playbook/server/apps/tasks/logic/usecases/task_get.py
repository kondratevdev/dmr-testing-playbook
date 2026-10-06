from __future__ import annotations

from typing import TYPE_CHECKING, final

import attrs
from django.contrib.auth.models import User

from server.apps.tasks.logic.value_objects import TaskFullPayload

if TYPE_CHECKING:
    from server.apps.tasks.infra import mappers, repository


@final
@attrs.define(slots=True, frozen=True)
class GetTask:
    """Get an existing task by its identifier."""

    _repository: repository.TaskRepository
    _mapper: mappers.TaskMapper

    def __call__(self, task_id: int, owner: User) -> TaskFullPayload:
        """Load and map a task."""
        return self._mapper.single(self._repository.get(task_id, owner))
