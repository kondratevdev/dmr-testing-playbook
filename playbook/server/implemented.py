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
        CompleteTask,
        CreateTask,
        GetTask,
        ListTasks,
    )
    from server.common import transactions

    inject = _create_injector(container, locals())  # noqa: WPS421
    # Common:
    container.register(transactions.TransactionAtomic)
    # Repositores:
    container.register(repository.TaskRepository)
    # Mappers:
    container.register(mappers.TaskMapper)
    # Usecases:
    container.register(inject(CreateTask))
    container.register(inject(GetTask))
    container.register(inject(ListTasks))
    container.register(inject(CompleteTask))


def populate_dependencies(container: punq.Container) -> punq.Container:
    """Populate dependencies for all project applications."""
    _inject_tasks(container)
    return container
