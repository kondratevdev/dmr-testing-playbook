from __future__ import annotations

from typing import TYPE_CHECKING, final

import attrs
from django.contrib.auth.models import User

from server.apps.tasks.logic.exceptions import TaskAlreadyCompletedError
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

    def __call__(self, task_id: int, owner: User) -> TaskFullPayload:
        """Complete and map a task."""
        with self._transaction():
            task = self._repository.get(task_id, owner, for_update=True)

            if task.is_completed:
                raise TaskAlreadyCompletedError

            return self._mapper.single(self._repository.complete(task))
