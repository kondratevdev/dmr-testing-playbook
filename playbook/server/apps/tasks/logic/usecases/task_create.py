from __future__ import annotations

from typing import TYPE_CHECKING, final

import attrs

from server.apps.tasks.logic.value_objects import (
    TaskCreatePayload,
    TaskFullPayload,
)

if TYPE_CHECKING:
    from server.apps.tasks.infra import mappers, repository


@final
@attrs.define(slots=True, frozen=True)
class CreateTask:
    """Create and return a task."""

    _repository: repository.TaskRepository
    _mapper: mappers.TaskMapper

    def __call__(self, payload: TaskCreatePayload) -> TaskFullPayload:
        """Persist a task and map it to its public representation."""
        return self._mapper(self._repository.create(payload))
