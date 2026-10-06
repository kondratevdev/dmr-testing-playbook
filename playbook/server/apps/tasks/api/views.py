from http import HTTPStatus
from typing import final, override

from django.contrib.auth.models import User
from django.http import HttpResponse
from dmr import Body, Controller, Path, Query, ResponseSpec, modify
from dmr.endpoint import Endpoint
from dmr.errors import ErrorType
from dmr.plugins.msgspec import MsgspecSerializer
from dmr.security import AuthenticatedHttpRequest
from dmr.security.jwt import HeaderJWTSyncAuth

from server.apps.tasks.logic.exceptions import TaskAlreadyCompletedError
from server.apps.tasks.logic.usecases import (
    CompleteTask,
    CreateTask,
    GetTask,
    ListTasks,
)
from server.apps.tasks.logic.value_objects import (
    TaskCreatePayload,
    TaskFullPayload,
    TaskListQuery,
    TaskPath,
)
from server.apps.tasks.models import Task
from server.common.di import HasContainer


@final
class TaskCreate(HasContainer, Controller[MsgspecSerializer]):
    """Manage the authenticated user's task collection.

    ``GET`` returns only tasks owned by the current user and can filter them
    by completion state. ``POST`` creates a task for that user; ownership is
    taken from the JWT, not from the request body.
    """

    auth = (HeaderJWTSyncAuth(),)
    request: AuthenticatedHttpRequest[User]

    def post(self, parsed_body: Body[TaskCreatePayload]) -> TaskFullPayload:
        """Create a task owned by the authenticated user."""
        return self.resolve(CreateTask)(
            parsed_body,
            self.request.user,
        )

    def get(
        self,
        parsed_query: Query[TaskListQuery],
    ) -> list[TaskFullPayload]:
        """List owned tasks, optionally filtered by completion state."""
        return self.resolve(ListTasks)(
            self.request.user,
            is_completed=parsed_query.is_completed,
        )


@final
class TaskDetail(HasContainer, Controller[MsgspecSerializer]):
    """Read and complete a task owned by the authenticated user.

    Both operations look up the task by ID within the user's own tasks, so
    missing and inaccessible tasks return the same not-found response.
    ``POST`` completes the task once and returns a conflict if it was already
    completed.
    """

    auth = (HeaderJWTSyncAuth(),)
    responses = (
        ResponseSpec(
            Controller.error_model,
            status_code=HTTPStatus.NOT_FOUND,
        ),
    )
    request: AuthenticatedHttpRequest[User]

    def get(self, parsed_path: Path[TaskPath]) -> TaskFullPayload:
        """Return an owned task or a not-found response."""
        return self.resolve(GetTask)(
            parsed_path.id,
            self.request.user,
        )

    @modify(
        status_code=HTTPStatus.OK,
        extra_responses=[
            ResponseSpec(
                Controller.error_model,
                status_code=HTTPStatus.CONFLICT,
            ),
        ],
    )
    def post(self, parsed_path: Path[TaskPath]) -> TaskFullPayload:
        """Complete an owned task, rejecting a repeated completion."""
        return self.resolve(CompleteTask)(
            parsed_path.id,
            self.request.user,
        )

    @override
    def handle_error(
        self,
        endpoint: Endpoint,
        controller: Controller[MsgspecSerializer],
        exc: Exception,
    ) -> HttpResponse:
        """Translate task lookup and state errors into API responses."""
        if isinstance(exc, Task.DoesNotExist):
            return self.to_error(
                self.format_error(
                    'Task not found',
                    error_type=ErrorType.not_found,
                ),
                status_code=HTTPStatus.NOT_FOUND,
            )
        if isinstance(exc, TaskAlreadyCompletedError):
            return self.to_error(
                self.format_error('Task already completed'),
                status_code=HTTPStatus.CONFLICT,
            )
        return super().handle_error(endpoint, controller, exc)
