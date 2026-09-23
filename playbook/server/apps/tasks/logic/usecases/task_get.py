from __future__ import annotations

from typing import TYPE_CHECKING, final

import attrs

from server.apps.tasks.logic.value_objects import TaskFullPayload

if TYPE_CHECKING:
    from server.apps.tasks.infra import mappers, repository


@final
@attrs.define(slots=True, frozen=True)
class GetTask:
    """Get an existing task by its identifier."""

    _repository: repository.TaskRepository
    _mapper: mappers.TaskMapper

    def __call__(self, task_id: int) -> TaskFullPayload:
        """Load and map a task."""
        return self._mapper(self._repository.get(task_id))
