from http import HTTPStatus
from typing import final, override

from django.http import HttpResponse
from dmr import Body, Controller, Path, modify
from dmr.endpoint import Endpoint
from dmr.errors import ErrorType
from dmr.plugins.msgspec import MsgspecSerializer

from server.apps.tasks.logic.usecases import (
    task_complete,
    task_create,
    task_get,
)
from server.apps.tasks.logic.value_objects import (
    TaskCreatePayload,
    TaskFullPayload,
    TaskPath,
)
from server.apps.tasks.models import Task
from server.common.di import HasContainer


@final
class TaskCreate(HasContainer, Controller[MsgspecSerializer]):
    """Create tasks."""

    def post(self, parsed_body: Body[TaskCreatePayload]) -> TaskFullPayload:
        """Create a task."""
        return self.resolve(task_create.CreateTask)(parsed_body)


@final
class TaskDetail(HasContainer, Controller[MsgspecSerializer]):
    """Fetch or complete a task addressed by a typed path DTO."""

    def get(self, parsed_path: Path[TaskPath]) -> TaskFullPayload:
        """Return an existing task."""
        return self.resolve(task_get.GetTask)(parsed_path.id)

    @modify(status_code=HTTPStatus.OK)
    def post(self, parsed_path: Path[TaskPath]) -> TaskFullPayload:
        """Mark an existing task as completed."""
        return self.resolve(task_complete.CompleteTask)(parsed_path.id)

    @override
    def handle_error(
        self,
        endpoint: Endpoint,
        controller: Controller[MsgspecSerializer],
        exc: Exception,
    ) -> HttpResponse:
        """Translate a missing ORM row into an API error."""
        if isinstance(exc, Task.DoesNotExist):
            return self.to_error(
                self.format_error(
                    'Task not found',
                    error_type=ErrorType.not_found,
                ),
                status_code=HTTPStatus.NOT_FOUND,
            )
        return super().handle_error(endpoint, controller, exc)
