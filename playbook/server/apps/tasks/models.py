from typing import final, override

from django.db import models

from server.apps.tasks.logic.constants import TASK_TITLE_MAX_LENGTH


@final
class Task(models.Model):
    """A task that can be completed exactly once."""

    title = models.CharField(max_length=TASK_TITLE_MAX_LENGTH)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    @override
    def __str__(self) -> str:
        """Return the human-readable task title."""
        return self.title  # pragma: no coverage
