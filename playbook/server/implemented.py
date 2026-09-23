from collections.abc import Callable
from typing import Any

import punq


def _create_injector[Thing](
    container: punq.Container,
    localns: dict[str, Any],
) -> Callable[[Thing], Thing]:
    """Teach punq how to resolve postponed annotations."""
    localns.pop('container')
    container.registrations._localns.update(localns)
    return lambda service: service


def _inject_tasks(container: punq.Container) -> None:
    from server.apps.tasks.infra import mappers, repository
    from server.apps.tasks.logic.usecases import (
        task_complete,
        task_create,
        task_get,
    )
    from server.common import transactions

    inject = _create_injector(container, locals())  # noqa: WPS421
    container.register(transactions.TransactionAtomic)
    container.register(repository.TaskRepository)
    container.register(mappers.TaskMapper)
    container.register(inject(task_create.CreateTask))
    container.register(inject(task_get.GetTask))
    container.register(inject(task_complete.CompleteTask))


def populate_dependencies(container: punq.Container) -> punq.Container:
    """Populate dependencies for all project applications."""
    _inject_tasks(container)
    return container
