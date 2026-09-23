from __future__ import annotations

from typing import TYPE_CHECKING, final

import attrs

from server.apps.tasks.logic.value_objects import TaskFullPayload

if TYPE_CHECKING:
    from server.apps.tasks.infra import mappers, repository
    from server.common.transactions import TransactionAtomic


@final
@attrs.define(slots=True, frozen=True)
class CompleteTask:
    """Mark an existing task as completed."""

    _repository: repository.TaskRepository
    _mapper: mappers.TaskMapper
    _transaction: TransactionAtomic

    def __call__(self, task_id: int) -> TaskFullPayload:
        """Complete and map a task."""
        with self._transaction():
            task = self._repository.get(task_id, for_update=True)
            return self._mapper(self._repository.complete(task))
