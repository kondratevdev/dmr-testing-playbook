import datetime as dt
from typing import Annotated, final

import msgspec

from server.apps.tasks.logic.constants import TASK_TITLE_MAX_LENGTH


class TaskCreatePayload(msgspec.Struct):
    """Input required to create a task."""

    title: Annotated[
        str,
        msgspec.Meta(min_length=1, max_length=TASK_TITLE_MAX_LENGTH),
    ]
    description: str = ''


@final
class TaskPath(msgspec.Struct):
    """Path parameters used to address a task."""

    id: Annotated[int, msgspec.Meta(gt=0)]


@final
class TaskFullPayload(TaskCreatePayload, kw_only=True):
    """Public representation of a persisted task."""

    id: int
    is_completed: bool
    created_at: dt.datetime
    completed_at: dt.datetime | None
